# expire_ordered_set
eoset support full `set` api. This structure can remember item insert order, and offer expire support for single item.  
Besides, eoset realize some interface which like handle list such as `__getitem__`, `__reversed__` and another pop method `pop_last`.

**expire method return value**
+ 0  *key not exist*
+ 1  *set timeout successfully*

**ttl method return value**
+ -2 *key not exist*
+ -1 *key exist and never expire*

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
