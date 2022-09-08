class Settings:

    def __init__(self, outdir: str):
        self.outdir = outdir


class Processor:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.outdir = self.settings.outdir
