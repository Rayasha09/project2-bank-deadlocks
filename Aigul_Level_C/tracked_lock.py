# Author: Abdullaeva Aigul
# Module 1  Блок C.
import threading
_guard=threading.RLock();_owners={};_waiting={}
def _cycle(start):
    seen=set();current=start
    while current in _waiting:
        if current in seen:return True
        seen.add(current)
        owner=_owners.get(_waiting[current])
        if owner is None:return False
        current=owner
    return False
class TrackedLock:
    def __init__(self,name):self.name=name;self.lock=threading.Lock()
    def acquire(self,blocking=True,timeout=-1):
        tid=threading.get_ident()
        with _guard:
            if _owners.get(self.name)==tid:raise RuntimeError('Повторный захват обычного Lock')
            if self.lock.locked() and blocking:
                _waiting[tid]=self.name
                if _cycle(tid):
                    _waiting.pop(tid,None)
                    raise RuntimeError('Обнаружена взаимоблокировка: цикл ожидания')
        try:
            got=self.lock.acquire(blocking,timeout) if blocking else self.lock.acquire(False)
            if got:
                with _guard:_owners[self.name]=tid
            return got
        finally:
            with _guard:_waiting.pop(tid,None)
    def release(self):
        tid=threading.get_ident()
        with _guard:
            if _owners.get(self.name)!=tid:raise RuntimeError('Не владелец блокировки')
            _owners.pop(self.name)
            self.lock.release()
    def __enter__(self):self.acquire();return self
    def __exit__(self,*args):self.release()
