from logger import Logger, LogLevels
import time
from threading import Thread

def log1():
    with Logger("session1") as log:
        log.write("Testing from thread\n")
        time.sleep(2)

def log2():
    logger = Logger("session2")
    logger.write("Testing from thread\n", LogLevels.LOW)
    time.sleep(2)

if __name__ == "__main__":
    t1 = Thread(target=log2) 
    t2 = Thread(target=log2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()