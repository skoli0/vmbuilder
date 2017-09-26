from vmimage import vmwindows as vmw
from vmimage import vmlinux as vml
#from vmwindows import vmwindows as VW

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
            vml.VMLinux(self.vm_dict)
        elif (self.vmos.lower() == 'windows'):
            self.vm_dict.pop('os', None)
            vmw.VMWindows(self.vm_dict)
        else:
            print("not a valid os type")

        print(self.vm_dict)
