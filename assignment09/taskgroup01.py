#example of aysncio task group
import asyncio

#coroutine task
async def task1():
    #report a message
    print("hello from coroutine 1")
    #sleep to simulate waitaing
    await asyncio.sleep(1)
    
#coroutine task
async def task2():
    #report message
    print("hello form coroutine 2")
    #sleep to simulate waitaing
    await asyncio.sleep(1)
    
#coroutine task
async def task3():
    #report message
    print("hello form coroutine 3")
    #sleep to simulate waitaing
    await asyncio.sleep(1)

#async entry point
async def main():
    async with asyncio.TaskGroup() as group:
        #run first task
        group.create_task(task1())
        #run second task
        group.create_task(task2())
        #run third task
        group.create_task(task3())
    #wait for all task to complete
    print("Done")
    
asyncio.run(main())