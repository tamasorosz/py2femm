from src.executor import RabbitExecutor
import asyncio

rmq = RabbitExecutor(script_files=[])

if __name__ == '__main__':

    # start workers
    asyncio.run(rmq.worker())
