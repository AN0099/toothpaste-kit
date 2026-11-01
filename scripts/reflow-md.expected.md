---
name: front-matter
desc: fixture for reflow-md.py --selftest, do not reformat this file
tags: one
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

Text right after the html block wraps and joins.

# Heading
Text right after a heading is its own paragraph.

####### seven hashes is not a heading.

***
Text after a rule.

A paragraph
# Heading that interrupts it

Paragraph before
1) a paren item

Paragraph before
+ a plus item

One trailing space does not break.

Paragraph before a fence
```
code
```

```
~~~
a tilde line does not close a backtick fence
```

  ```
  indented fence
  stays put
  ```

Short underline
--

Indented setext
===

- item then rule continued
---

- item then lazy line
lazy line stays

- item then one-space line
 one-space line stays

- item then a lazy line
lazy
then an indented one
---

- item before a fence
```
code
```
Indented title after fence
---

- item before a heading
# Heading
Indented title after heading
---

Two blank lines above collapse to one.
