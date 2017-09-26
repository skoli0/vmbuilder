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

class VMWindows(VMImage):
    def __init__(self, vm):
        super().__init__(vm)
        print("build windows " + vm['image'])

class BuildVM(object):
    def __init__(self, vm_dict):
        self.image = vm_dict['image']
        self.vmuser = vm_dict['user']
        self.vmos = vm_dict['os']
        self.vmarch = vm_dict['arch']
        self.vmiso = vm_dict['iso']
        self.vm_dict = vm_dict

    def Build(self):
        #print(self.vmuser)
        if (self.vmos.lower() == 'linux'):
            self.vm_dict.pop('os', None)
            VMLinux(self.vm_dict)
        elif (self.vmos.lower() == 'windows'):
            self.vm_dict.pop('os', None)
            VMWindows(self.vm_dict)
        else:
            print("not a valid os type")

        print(self.vm_dict)
