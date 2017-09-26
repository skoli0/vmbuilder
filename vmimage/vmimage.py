#from vmimage import *

class VMImage(object):
    def __init__(self, vm):
        #print('VMImage class is defined')
        #self.os = _os
        self.arch = vm['arch']
        self.iso = vm['iso']

    def answerfile(self):
        print("answerfile")

    def packerfile(self):
        print("packerfile")

    def preprocess(self):
        print("preprocess")

    def validate(self):
        print("validate")

    def build(self):
        print("build")

    def cleanup(self):
        print("cleanup")

    def buildimage(self):
        self.answerfile()
        self.packerfile()
        self.preprocess()
        self.validate()
        self.build()
        self.cleanup()

    def __str__(self):
        return self.os + ", " + self.arch

class VMLinux(VMImage):
    def __init__(self, vm):
        super().__init__(vm)
        print("build linux " + vm['image'])
