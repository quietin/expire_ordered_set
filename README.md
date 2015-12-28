# expire_ordered_set
eoset can remember item insert order, and offer expire support for single item.  
Besides, eoset realize some interface which like handle list such as `pop_last`, `__getitem__`, `__reversed__`

e.g.
```python
from eoset import eoset
import time

item = eoset('jljfsdfadf')
print item
print reversed(item)
print item[3]

print item.pop()
print item.pop_last()
print item

item.expires(50)
print item.ttls()
item.expire('d', 4)
print item.ttl('d')
time.sleep(5)
print item.ttl('d')
```
