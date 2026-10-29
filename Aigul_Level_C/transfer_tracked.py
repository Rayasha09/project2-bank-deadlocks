# Автор: участник 4 (впишите имя). Проверка блока C.
import threading,faulthandler,time
from tracked_lock import TrackedLock
faulthandler.dump_traceback_later(3,exit=True)
locks={'A':TrackedLock('A'),'B':TrackedLock('B')}
barrier=threading.Barrier(2)
def worker(src,dst):
    try:
        with locks[src]:
            barrier.wait()
            with locks[dst]:pass
    except RuntimeError as e:print(threading.current_thread().name,e,flush=True)
t1=threading.Thread(target=worker,args=('A','B'),name='cashier1')
t2=threading.Thread(target=worker,args=('B','A'),name='cashier2')
t1.start();t2.start();t1.join();t2.join()
faulthandler.cancel_dump_traceback_later()
print('TrackedLock test completed')
