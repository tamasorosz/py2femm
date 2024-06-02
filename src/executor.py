"""
Runs the FEMM on the given environment: windows or with wine under a linux environment.
The created models runs as input files.
"""
from sys import platform
from threading import Timer
import subprocess
from pathlib import Path


class Executor:
    # using wine under linux environment
    femm_path_linux = str(Path.home()) + "/.wine/drive_c/femm42/bin/femm.exe"
    femm_path_windows = r"D:\femm42\bin\femm.exe"

    def run(self, script_file, timeout=1000, debug=False):
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

