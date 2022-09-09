import os


class ImageProcess:
    def __init__(self, path):
        self.path = path

    def mkdir(self):
        exist = os.path.exists(self.path)

        if not exist:
            os.makedirs(self.path)
        else:
            print('folder exists')
