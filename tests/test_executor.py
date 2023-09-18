from unittest import TestCase
from src.executor import Executor
from importlib.resources import files
import os
import warnings


class TestExecutor(TestCase):

    def test_executor(self):
        testfile = files('tests').joinpath("test_files").joinpath("invalid.lua")
        print(testfile)

        warnings.simplefilter("ignore", ResourceWarning)
        femm = Executor()

        with open(testfile, "w") as f:
            f.write("not_existing_command()")

        home = os.path.expanduser("~")
        ref_cmd = f"wine {home}/.wine/drive_c/femm42/bin/femm.exe -lua-script={home}"
        ref_cmd_end = f"/tests/test_files/invalid.lua"

        test_cmd = femm.run(testfile, debug=True)
        # test part 1
        self.assertIn(ref_cmd, test_cmd)

        # test part 2
        self.assertIn(ref_cmd_end, test_cmd)
