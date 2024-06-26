# Synchronous cooking
# 1 kitchen 1 chefs 1 dish
from time import sleep, ctime, time

#cooking synchronous
def cooking(index):
    print(f'{ctime()} Kitchen-{index}  : Begin cooking...')
    sleep(2)
    print(f'{ctime()} Kitchen-{index}  : cooking done')

if __name__=="__main__":
    # Begin of main thread
    print(f'{ctime()} Main       : start cooking')
    start_time = time()
    #cooking
    cooking(0)
    
    duration = time() - start_time
    print(f"{ctime()} main    : Finished cooking duration in {duration:0.2f} seconds")    