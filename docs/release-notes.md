---
hide:
  - navigation
---


```python exec="on"

import os

filename = 'CHANGELOG.md'

if os.path.isfile(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        content = (
            content.replace("# Changelog", "")
            .replace("[GitHub Release]", "[:material-github: GitHub Release]")
            .replace("[Full Changelog]", "[:material-source-pull: Full Changelog]")
        )
        print(content)
else:
    raise FileNotFoundError("File 'CHANGELOG.md' not found")

```