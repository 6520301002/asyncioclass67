from random import random
import asyncio

async def task_rice():
    
    value = 1+random()
    await asyncio.sleep(1)
    print(f'>ricecooking {value}')
    return value
    
async def task_noodle():
   
    value = 1+random()
    await asyncio.sleep(1)
    print(f'>noodle cooking {value}')
    return value
    
async def task_curry():

    value = 1+random()
    await asyncio.sleep(1)
    print(f'>curry cooking {value}')
    return value
    
async def main():
    tasks = [asyncio.create_task(task_rice(),name='rice'),
            asyncio.create_task(task_noodle(),name='noodle'),
            asyncio.create_task(task_curry(),name='curry')]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    print("finished cooking")
    first = done.pop()
    print(first.get_name(),"cooking completed",(first.result()))
    

asyncio.run(main())