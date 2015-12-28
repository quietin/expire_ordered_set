# expire_ordered_set
eoset can remember item insert order, and offer expire support for single item.  
Besides, eoset realize some interface which like handle list such as `pop_last`, `__getitem__`, `__reversed__`

e.g.
```python
from eoset import eoset
import time

item = eoset('jljfsdfadf')
print item
# ExpireOrderSet(['j', 'l', 'f', 's', 'd', 'a'])
print reversed(item)
# ExpireOrderSet(['a', 'd', 's', 'f', 'l', 'j'])
print item[3]
# s

print item.pop()  # j
print item.pop_last() # a
print item
# ExpireOrderSet(['l', 'f', 's', 'd'])

item.expires(50)
print item.ttls()
# [('d', '50.0000'), ('s', '50.0000'), ('l', '50.0000'), ('f', '50.0000')]
item.expire('d', 4)
print item.ttl('d')
# 4.0000
time.sleep(5)
print item.ttl('d')
# -2
```
