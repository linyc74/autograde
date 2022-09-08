import os
import shutil
import unittest
from typing import Tuple
from autograde.template import Settings


def get_dirs(py_path: str) -> Tuple[str, str]:
    indir = os.path.relpath(path=py_path[:-3], start=os.getcwd())
    basedir = os.path.dirname(indir)
    outdir = os.path.join(basedir, 'outdir')
    return indir, outdir


class TestCase(unittest.TestCase):

    def set_up(self, py_path: str):
        self.indir, self.outdir = get_dirs(py_path=py_path)
        self.settings = Settings(outdir=self.outdir)
        os.makedirs(self.outdir, exist_ok=True)

    def tear_down(self):
        shutil.rmtree(self.outdir)

    def assertFileEqual(self, first: str, second: str):
        with open(first) as fh1:
            with open(second) as fh2:
                self.assertEqual(fh1.read(), fh2.read())
