from abc import ABCMeta, abstractmethod
import os.path
import cv2


class AbstractSim(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.frames = []

    @abstractmethod
    def get_state_image(self, ind):
        """to override"""
        pass

    def generate_video(self, filename, fps):
        if len(self.frames) < 1:
            raise Exception(
                'State was not saved during simulation. Cannot generate video.'
            )
        mat = self.get_state_image(0)
        height, width, layers = mat.shape
        size = (width, height)

        out = cv2.VideoWriter(os.path.join(os.path.curdir, filename), cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
        out.write(cv2.cvtColor(mat, cv2.COLOR_RGBA2BGR))
        for i in range(1, len(self.frames)):
            img = self.get_state_image(i)
            out.write(cv2.cvtColor(img, cv2.COLOR_RGBA2BGR))
            self.print_status_bar(i, len(self.frames), prefix='Video generation')
        cv2.destroyAllWindows()
        out.release()

    @staticmethod
    def print_status_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        if iteration == total:
            print()
