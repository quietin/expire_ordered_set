# expire_ordered_set
[![](https://travis-ci.org/quietin/expire_ordered_set.svg?branch=master)](https://travis-ci.org/quietin/expire_ordered_set)

eoset support full `set` api. This structure can remember item insert order, and offer expire support for single item.  
Besides, eoset realize some interface which like handle list such as `__getitem__`, `__reversed__` and another pop method `pop_last`.

**expire method return value**
+ 0 :  *key not exist*
+ 1 :  *set timeout successfully*

**ttl method return value**
+ -2 : *key not exist*
+ -1 : *key exist and never expire*

e.g.
```bash
python -i eoset.py
```
and then
```python
>>> item = eoset('jljfsdfadf')
>>> reversed(item)
<listreverseiterator at 0x101fa3710>
>>> item[3]
's'
>>> item.pop()
'j'
>>> item.pop_last()
'a'
>>> item
ExpireOrderSet(['l', 'f', 's', 'd'])
>>> item.expires(50)
>>> item.ttls()
[('d', '43.6890'), ('s', '43.6890'), ('l', '43.6890'), ('f', '43.6890')]
>>> item.expire('d', 20)
1
>>> item.ttl('d')
'15.5761'
>>> time.sleep(16)
>>> item.ttl('d')
-2
```
