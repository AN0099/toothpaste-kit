# CHANGELOG

## v1 (split from working-preferences)

Created when `working-preferences` v8 was split in two. That file holds the general behavior every
adopter gets; this one holds the maintainer's own opinions on top of it, so the kit installed whole
behaves as the maintainer's own setup does, while `scripts/link-skills.sh --base` installs without
them.

**Why a layer rather than a fork or a deletion.** Some of these opinions are useful to others, and
dropping them would leave the shipped kit behaving differently from the setup it was built from. A
layer keeps them shipped and readable, and lets an adopter swap in their own in their place, the way
a distribution keeps its opinionated defaults in a named layer over a general base.

The Role line, Input Syntax and Reply Cost moved unchanged. The brevity code and context cadence
sections hold the reasons `working-preferences` gave before v8, unchanged except where the `j` row's
removal made "the six most used" and "three per hand" untrue.

The banded context table moved too. It was the v5 fix for a session that ran far past the
degradation point; `working-preferences` now states the cadence's rules without numbers.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
