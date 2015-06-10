# lfu-cache

Cache with LFU eviction scheme implemented in Python with complexity O(1) for insertion, access and deletion.

```python
>>> import lfucache.lfu_cache as lfu_cache

>>> cache = lfu_cache.Cache()

>>> cache.insert('k1', 'v1')
>>> cache.insert('k2', 'v2')
>>> cache.insert('k3', 'v3')
>>> cache.display_lists()
1: ['k1', 'k2', 'k3']

>>> cache.access('k2')
'v2'
>>> cache.display_lists()
1: ['k1', 'k3']
2: ['k2']

>>> cache.get_lfu()
('k1', 'v1')

>>> cache.delete_lfu()
>>> cache.display_lists()
1: ['k3']
2: ['k2']
```
