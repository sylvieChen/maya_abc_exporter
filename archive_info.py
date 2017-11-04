import alembic


FPS = 24.0


class ArchiveInfo(object):
    def __init__(self):
        super(ArchiveInfo, self).__init__()

        self.fps = FPS
        self.start_frame = 1001
        self.end_frame = 1001
        self.timePerCycle = 1 / self.fps
        self.startTime = self.start_frame / self.fps
        self.ts = alembic.AbcCoreAbstract.TimeSampling(self.timePerCycle, self.startTime)

