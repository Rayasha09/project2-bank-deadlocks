# Автор: участник 4 (впишите имя). Блок C, 5 философов.
import threading,time,sys,statistics
N=5;ROUNDS=10

def experiment(mode):
    forks=[threading.Lock() for _ in range(N)]
    waiter=threading.Semaphore(4) if mode=='waiter' else None
    barrier=threading.Barrier(N) if mode=='naive' else None
    counts=[0]*N;maxwait=[0.0]*N
    def philosopher(i):
        left,right=i,(i+1)%N
        for _ in range(ROUNDS):
            start=time.monotonic()
            if waiter:waiter.acquire()
            first,second=(left,right)
            if mode=='ordered':first,second=sorted((left,right))
            with forks[first]:
                if barrier:barrier.wait()
                with forks[second]:
                    wait=time.monotonic()-start
                    maxwait[i]=max(maxwait[i],wait)
                    counts[i]+=1
            if waiter:waiter.release()
    threads=[threading.Thread(target=philosopher,args=(i,),daemon=True) for i in range(N)]
    for t in threads:t.start()
    for t in threads:t.join(timeout=1.0 if mode=='naive' else 5.0)
    stuck=sum(t.is_alive() for t in threads)
    print(mode,'eaten=',counts,'stuck=',stuck,'max_wait_seconds=',round(max(maxwait),6))
    return stuck
if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'ordered'
    if mode not in ('naive','ordered','waiter'):raise SystemExit('Use naive|ordered|waiter')
    experiment(mode)
