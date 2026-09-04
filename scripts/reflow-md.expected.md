---
name: front-matter
desc: fixture for reflow-md.py --selftest, do not reformat this file
---

# Heading

A wrapped paragraph that should join.

Setext Heading
==============

Another wrapped paragraph.

- a list item that wraps onto a second line
- a second item
  1. nested ordered with continuation

```bash
echo "line one"
echo "line two"
if [ -f x ]; then
  echo nested
fi
```

| col | col |
|---|---|
| a | b |

> a blockquote line
> a second one

---

~~~
tilde fence
second line
~~~

A line ending in two spaces  
must stay broken here.

<div>
  <p>html block</p>
</div>
