from .vmimage import *

class VMWindows(VMImage):
    def __init__(self, vm):
        super().__init__(vm)
        #self.vm = vm

    def Build(self):
        #print("build windows " + self.vm['image'])
        self.buildimage()
