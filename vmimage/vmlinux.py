from .vmimage import *

class VMLinux(VMImage):
    def __init__(self, vm):
        super().__init__(vm)
        #self.vm = vm

    def Build(self):
        #print("build linux " + self.vm['image'])
        self.buildimage()
