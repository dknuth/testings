import random, time
import threading
from threading import Thread, Lock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import models
from models import Base, User


NRROW=10
NRTHREAD=300


class Produce(Thread):
    def __init__(self, seq):
        Thread.__init__(self)
        self.daemon = True
        self.seq = seq
    
    def run(self):
        obj = User('user_%03d'%self.seq, random.randrange(10, 90))
        session.add(obj)
        session.commit()



class Update(Thread):
    def __init__(self, seq):
        Thread.__init__(self)
        self.daemon = True
        self.seq = seq
    
    def run(self):
        time.sleep(3)

        lock.acquire()
        obj = session.query(User).get(1)
        obj.name = 'update_user_%03d' % random.randrange(1, NRROW+1)
        obj.seq = obj.seq + 1
        session.add(obj)
        session.commit()
        lock.release()



def main():
    __builtins__.engine = create_engine('postgresql://sample:sample@localhost/sample')
    __builtins__.session = scoped_session(
        sessionmaker(
            autoflush = False,
            autocommit = False,
            bind = engine)
        )
    __builtins__.lock = Lock()
    Base.metadata.create_all(engine)

    for i in range(NRROW):
        Produce(i).start()

    while threading.active_count() != 1:
        time.sleep(0.1)

    for i in range(NRTHREAD):
        Update(i).start()

    while threading.active_count() != 1:
        time.sleep(0.1)



if __name__ == '__main__':
    main()
    print "Terminated..."
    
