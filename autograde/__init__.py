import os
from .template import Settings
from .autograde import Autograde


__version__ = '1.0.1-beta'


def autograde(
        standard_dir: str,
        student_dir: str,
        outdir: str):

    os.makedirs(outdir, exist_ok=True)
    settings = Settings(outdir=outdir)

    Autograde(settings=settings).main(
        standard_dir=standard_dir,
        student_dir=student_dir)
