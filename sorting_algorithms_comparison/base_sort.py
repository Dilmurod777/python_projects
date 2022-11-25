class Base:
    def __init__(self):
        self.array = []

    def sort(self, *args):
        pass

    def run(self, array):
        self.array = array.copy()
        self.sort()
        return self.array
