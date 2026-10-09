#!/bin/bash
# Classify a git repository by WHERE its remotes point, not by whether it
# has one.
#
# "Has a remote" is a poor proxy for "can publish": a bare repository on a
# machine in your own network reaches nobody outside it, and pushing there
# publishes nothing. So the level is read from each remote's address.
#
#   none      no remote                          an agent may commit
#   internal  private address space or a path    commit and push to its own branch
#   external  anything else, GitHub included     read, edit and stage only
#
# The right-hand column is the policy skills/merge-proxy/ assumes; adapt it to
# your own project instructions.
#
# THE DEFAULT IS external. A host that cannot be PROVEN internal is treated as
# publication, because the two failures are not symmetric: a wrong `internal`
# pushes to the internet, and a wrong `external` is a refusal a person can
# override in a second. That is why a hostname like `nas.local` classifies as
# external rather than being guessed at. Add addresses, not names.
#
#   remote-level.sh PATH        print the level
#   remote-level.sh --selftest  prove all three answers, both directions

url_class() {
    local url="$1" host=""
    case "$url" in
        /*|./*|../*|file://*)  echo internal; return ;;
        ssh://*|git://*|http://*|https://*)
            host="${url#*://}"; host="${host#*@}"
            host="${host%%/*}";  host="${host%%:*}" ;;
        *@*:*)  host="${url#*@}"; host="${host%%:*}" ;;
        *:*)    host="${url%%:*}" ;;
        *)      echo external; return ;;
    esac
    case "$host" in localhost|::1) echo internal; return ;; esac
    # A range prefix means an address only when the whole host is four dotted
    # numbers. 192.168.50.10.example.com starts like one and is a public name.
    if ! [[ "$host" =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]]; then echo external; return; fi
    case "$host" in
        127.*)                 echo internal ;;
        192.168.*|10.*)        echo internal ;;
        172.1[6-9].*|172.2[0-9].*|172.3[0-1].*)  echo internal ;;
        100.6[4-9].*|100.[7-9][0-9].*|100.1[0-1][0-9].*|100.12[0-7].*)
                               echo internal ;;
        *)                     echo external ;;
    esac
}

repo_level() {
    local repo="$1" urls u level="internal"
    # A path that is not a repository has no remotes to read, and "no remotes"
    # is the most permissive answer. Refuse it as external instead, the same
    # asymmetry the header argues.
    if ! git -C "$repo" rev-parse --git-dir >/dev/null 2>&1; then
        echo "remote-level: not a git repository: $repo" >&2
        echo external; return
    fi
    urls="$(git -C "$repo" remote -v 2>/dev/null | awk '{print $2}' | sort -u)"
    [ -z "$urls" ] && { echo none; return; }
    while IFS= read -r u; do
        [ -z "$u" ] && continue
        [ "$(url_class "$u")" = external ] && level="external"
    done <<< "$urls"
    echo "$level"
}

_selftest() {
    local pass=0 fail=0
    # NOT local: the EXIT trap fires after this function returns, and a local
    # is out of scope by then, which under set -u is an error on the way out.
    _RL_TMP="$(mktemp -d)"; trap 'rm -rf "$_RL_TMP"' EXIT
    check() {  # name expected url...
        local name="$1" want="$2"; shift 2
        local d="$_RL_TMP/$name"; mkdir -p "$d"; git -C "$d" init -q 2>/dev/null
        local i=0; for u in "$@"; do git -C "$d" remote add "r$i" "$u"; i=$((i+1)); done
        local got; got="$(repo_level "$d")"
        if [ "$got" = "$want" ]; then pass=$((pass+1))
            [ -n "${RL_VERBOSE:-}" ] && printf '  ok   %-22s %s\n' "$name" "$got"
        else fail=$((fail+1)); printf '  FAIL %-22s want %s got %s\n' "$name" "$want" "$got"; fi
        return 0
    }
    check no-remote        none
    check local-path       internal /srv/git/project.git
    check relative-path    internal ../project.git
    check lan-scp          internal 192.168.50.7:/srv/git/project.git
    check lan-ssh-url      internal ssh://192.168.50.7/srv/git/project.git
    check lan-https        internal https://192.168.50.7/x.git
    check tailnet          internal 100.100.1.2:/x.git
    check rfc1918-10       internal 10.0.0.5:/x.git
    check github-https     external https://github.com/example/project.git
    check github-scp       external git@github.com:example/project.git
    check unknown-hostname external nas.local:/x.git
    check public-ipv4      external https://203.0.113.5/x.git
    check mixed-wins-worst external /srv/git/project.git https://github.com/example/project.git
    check range-prefix-name external https://192.168.50.10.example.com/x.git
    check ten-prefix-name  external git@10.example.com:x.git
    check cgnat-prefix-name external ssh://100.64.0.1.attacker.net/x.git
    local got
    got="$(repo_level "$_RL_TMP/does-not-exist" 2>/dev/null)"
    if [ "$got" = external ]; then pass=$((pass+1)); [ -n "${RL_VERBOSE:-}" ] && printf '  ok   %-22s %s\n' missing-path "$got"
    else fail=$((fail+1)); printf '  FAIL %-22s want external got %s\n' missing-path "$got"; fi
    mkdir -p "$_RL_TMP/not-a-repo"
    got="$(repo_level "$_RL_TMP/not-a-repo" 2>/dev/null)"
    if [ "$got" = external ]; then pass=$((pass+1)); [ -n "${RL_VERBOSE:-}" ] && printf '  ok   %-22s %s\n' not-a-repo "$got"
    else fail=$((fail+1)); printf '  FAIL %-22s want external got %s\n' not-a-repo "$got"; fi
    echo "remote-level: $pass passed, $fail failed (18 cases, all three levels)"
    [ "$fail" -eq 0 ]
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    set -uo pipefail
    case "${1:-}" in
        --selftest) _selftest ;;
        "") echo "usage: remote-level.sh PATH | --selftest" >&2; exit 2 ;;
        *)  repo_level "$1" ;;
    esac
fi
