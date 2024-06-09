"""
Runs the FEMM on the given environment: windows or with wine under a linux environment.
The created models runs as input files.
"""
from sys import platform
from threading import Timer
import subprocess
from pathlib import Path

import asyncio
from patio import Registry, ProcessPoolExecutor, NullExecutor
from patio_rabbitmq import RabbitMQBroker


class Executor:
    # using wine under linux environment
    femm_path_linux = str(Path.home()) + "/.wine/drive_c/femm42/bin/femm.exe"
    femm_path_windows = r"D:\femm42\bin\femm.exe"

    def run(self, script_file, timeout=1000):
        command = []
        script_file = Path(script_file).resolve()
        assert script_file.exists(), f"{script_file} does not exists."

        if platform == "linux":
            command.append("wine")
            command.append(self.femm_path_linux)
            command.append(f"-lua-script={script_file}")

        elif platform == "win32":
            command.append(self.femm_path_windows)
            command.append(f"-lua-script={script_file}")
            command.append("-windowhide")

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_timer = Timer(timeout, proc.kill)
        try:
            process_timer.start()
            proc.communicate()
            proc.wait(timeout=timeout)
        finally:
            process_timer.cancel()


class RabbitExecutor:

    def __init__(self, name="py2femm-rabbitmq", script_files=[]):
        self.rpc = Registry(project=name, auto_naming=False)
        self.scripts = script_files
        self.executor = Executor()
        self.rpc['runner'] = self.executor.run

    async def worker(self):
        async with ProcessPoolExecutor(self.rpc, max_workers=4) as executor:
            async with RabbitMQBroker(
                    executor, amqp_url="amqp://guest:guest@localhost/",
            ) as broker:
                await broker.join()

    async def broker(self):
        async with NullExecutor(Registry(project="py2femm-rabbitmq")) as executor:
            async with RabbitMQBroker(executor, amqp_url="amqp://guest:guest@localhost/", ) as broker:
                print(
                    await asyncio.gather(
                        *[
                            broker.call("runner", file, timeout=1) for file in self.scripts
                        ]
                    ),
                )


if __name__ == '__main__':

    rmq = RabbitExecutor(script_files=[])
    print("Run RabbitMq workers...")
    # start workers
    asyncio.run(rmq.worker())
