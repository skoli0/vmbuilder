from .vmimage import *

class VMWindows(VMImage):
    def __init__(self, vm):
        super().__init__(vm)
        print("build windows " + vm['image'])
