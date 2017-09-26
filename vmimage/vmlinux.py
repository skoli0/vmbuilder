from .vmimage import *

class VMLinux(VMImage):
    def __init__(self, vm):
        super().__init__(vm)
        print("build linux " + vm['image'])
