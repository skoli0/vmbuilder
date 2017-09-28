from vmimage import vmwindows as vmw
from vmimage import vmlinux as vml

class BuildVM(object):
    """
    # Wrapper class around actual OS specific classes
    # All the argument validation will be done here to reduce overhead on
    # actual image classes
    """
    def __init__(self, vm_dict):
        self.image = vm_dict['image']
        self.vmuser = vm_dict['user']
        self.vmos = vm_dict['os']
        self.vmarch = vm_dict['arch']
        self.vmiso = vm_dict['iso']
        self.vm_dict = vm_dict

    def Build(self):
        #print(self.vmuser)
        if ('linux' in self.vmos.lower()):
            #self.vm_dict.pop('os', None)
            vm = vml.VMLinux(self.vm_dict)
            vm.Build()
        elif ('windows' in self.vmos.lower()):
            #self.vm_dict.pop('os', None)
            vm = vmw.VMWindows(self.vm_dict)
            vm.Build()
        else:
            print("not a valid os type")

        print(self.vm_dict)
