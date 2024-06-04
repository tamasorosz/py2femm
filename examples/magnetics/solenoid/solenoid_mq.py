from solenoid import solenoid
from src.executor import RabbitExecutor
from os import getcwd
import asyncio

problem = solenoid(2, 2, 2, 6, 1)

current_dir = getcwd()
lua_file = current_dir + "/solenoid.lua"

rmq = RabbitExecutor(script_files=[lua_file])

if __name__ == '__main__':

    # create a producer which sends the tasks to the workers
    asyncio.run(rmq.broker())
