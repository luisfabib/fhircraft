---
icon: lucide/drafting-compass
---


```python exec="on"

import os

filename = 'CODE_OF_CONDUCT.md'

if os.path.isfile(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
else:
    raise FileNotFoundError("File 'CODE_OF_CONDUCT.md' not found")


```