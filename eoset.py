from time import time
from collections import MutableSet, OrderedDict
from threading import RLock

__all__ = ['eoset']


class ExpireOrderSet(MutableSet):
    def __init__(self, iterable=None):
        """fromkeys default value is None which represents never expire"""
        self._time_map = OrderedDict()
        self._lock = RLock()
        if iterable is not None:
            if isinstance(iterable, OrderedDict):
                self._time_map = iterable
            else:
                self._time_map = OrderedDict.fromkeys(iterable)

    def expire(self, key, ttl):
        """
        :param key: str
        :param ttl: int or long or float, units are seconds
        :return: 1 if the timeout was set, 0 if key does not exist
        """
        assert isinstance(ttl, (int, long, float))
        with self._lock:
            try:
                expire_time = self._time_map[key]
                if not expire_time:
                    self._time_map[key] = time() + ttl
                    return 1
                rest_time = expire_time - time()
                if rest_time > 0:
                    if ttl <= 0:
                        self._time_map[key] = None
                    else:
                        self._time_map[key] = time() + ttl
                    return 1
                else:
                    del self._time_map[key]
            except KeyError:
                pass

            return 0

    def expires(self, ttl):
        assert isinstance(ttl, (int, long, float))
        with self._lock:
            for key in self._time_map.iterkeys():
                self.expire(key, ttl)

    @staticmethod
    def _format_time(t):
        return '{:.4f}'.format(t)

    def __del_expire_keys(self):
        with self._lock:
            for k, v in self._time_map.iteritems():
                if v and v - time() <= 0:
                    del self._time_map[k]

    def ttl(self, key):
        """returns -2 if the key does not exist.
        returns -1 if the key exists but has no associated expire
        """
        with self._lock:
            try:
                key_val = self._time_map[key]
                if not key_val:
                    return -1
                rest_time = key_val - time()
                if rest_time > 0:
                    return self._format_time(rest_time)
                else:
                    del self._time_map[key]
            except KeyError:
                pass

            return -2

    def ttls(self):
        with self._lock:
            self.__del_expire_keys()
            ttl_map = {}
            for k, v in self._time_map.iteritems():
                if v:
                    ttl_map[k] = self._format_time(v - time())
                else:
                    ttl_map[k] = v
            return ttl_map.items()

    def add(self, value):
        with self._lock:
            if value not in self._time_map.iterkeys():
                self._time_map.update({value: None})

    def discard(self, value):
        with self._lock:
            try:
                del self._time_map[value]
            except KeyError:
                pass

    def __getitem__(self, item):
        """make set can get item from index"""
        with self._lock:
            try:
                return self._time_map.keys()[item]
            except IndexError:
                raise IndexError('set index out of range')

    def __reversed__(self):
        with self._lock:
            self.__del_expire_keys()
            return self.__class__(OrderedDict(reversed(self._time_map)))

    def pop_last(self):
        """Return the popped value.  Raise KeyError if empty."""
        it = iter(self)
        first = True
        value = None
        while True:
            try:
                value = next(it)
                first = False
            except StopIteration:
                if first:
                    raise KeyError
                break
        self.discard(value)
        return value

    def __contains__(self, key):
        with self._lock:
            try:
                ttl = self._time_map[key]
                if not ttl:
                    return True
                rest_time = ttl - time()
                if rest_time > 0:
                    return True
                else:
                    del self._time_map[key]
            except KeyError:
                pass

            return False

    def __iter__(self):
        for x in self._time_map.iterkeys():
            yield x

    def __len__(self):
        return len(self._time_map)

    def __repr__(self):
        with self._lock:
            cls_name = self.__class__.__name__
            if not self:
                return '%s()' % cls_name

            self.__del_expire_keys()
            return '%s(%r)' % (cls_name, self._time_map.keys())


eoset = ExpireOrderSet
