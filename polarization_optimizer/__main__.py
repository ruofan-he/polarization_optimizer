from . import Random_Walk_Handler
from time import sleep

if __name__ == '__main__':
    random_walk_handler = Random_Walk_Handler()
    while True:
        random_walk_handler.step()
        sleep(0.001)
