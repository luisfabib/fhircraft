---
icon: lucide/scale
---


```python exec="on"

import os

filename = 'LICENSE'

if os.path.isfile(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
else:
    raise FileNotFoundError("File 'LICENSE' not found")



```