import os
import shutil
from packer.packer import *

PACKER_TEMPLATES_DIR = "templates"
INPUT_ARTIFACTS_DIR = "input-artifacts"
OUTPUT_ARTIFACTS_DIR = "output-artifacts"

class VMImage(object):
    def __init__(self, vm, osfamily):
        #print('VMImage class is defined')
        self.user = vm['user']
        self.password = vm['pass']
        self.osname = vm['os']
        self.osfamily = osfamily
        self.arch = vm['arch']
        self.iso = vm['iso']
        self.hypervisor = vm['hypervisor']
        self.ram = vm['ram']
        self.disk = int(vm['disk']) * 1024
        self.language = vm['language']
        self.displayname = "{0} {1}bit {2}".format(self.osname, self.arch, self.language).title()
        #print(self.displayname)
        self.vm_dir = self.displayname.lower().replace(' ', '_')
        #print(self.osname, self.osfamily)
        self.vmindir = os.path.abspath(os.path.join(INPUT_ARTIFACTS_DIR, self.hypervisor, self.osfamily, self.vm_dir).lower())
        #print(self.vmindir)
        self.vmoutdir = os.path.abspath(os.path.join(OUTPUT_ARTIFACTS_DIR, self.hypervisor, self.osfamily, self.vm_dir).lower())
        #print(self.vmoutdir)

        self.steps = ['answerfile',
                      'packerfile',
                      'preprocess',
                      'validate',
                      'build',
                      'cleanup',
                      'all'
                      ]

    def answerfile(self):
        print("answerfile")

    def packerfile(self):
        print("packerfile")

    def preprocess(self):
        print("preprocess")

    def validate(self):
        self.packer = Packer(self.vm_packerfile, only=[self.hypervisor + '-iso'])
        self.packer.validate(syntax_only=False)

    def build(self):
        print("build")
        self.packer.build(force=True)

    def cleanup(self):
        print("cleanup")

    def buildimage(self):
        self.answerfile()
        self.packerfile()
        self.preprocess()
        self.validate()
        #self.build()
        #self.cleanup()

    def get_packerfile(self):
        """Returns the os-specific packer json template file

        :param os_type: target image os
        :return: os specific packer json template
        """
        packerfile = os.path.join(PACKER_TEMPLATES_DIR, self.osfamily, self.osfamily + "_packerfile.json")

        if not os.path.isfile(packerfile):
            raise OSError('packerfile not found at path: {0}'.format(packerfile))

        return packerfile.replace('\\', '/')

    def get_answerfile(self, os_type):
        """Returns the os-specific packer answer template file

        :param os_type: target image os
        :return: os specific packer json template
        """
        sif_answerfile = os.path.abspath(os.path.join(PACKER_TEMPLATES_DIR, self.osfamily, "winnt.sif"))
        xml_answerfile = os.path.abspath(os.path.join(PACKER_TEMPLATES_DIR, self.osfamily, "autounattend.xml"))
        print(sif_answerfile, xml_answerfile)

        try:
            answerfiles = [sif_answerfile, xml_answerfile];
            if all([os.path.isfile(f) for f in answerfiles]):
                return answerfiles
        except (OSError, IOError, TypeError) as e:
            logging.error('packer config file does not exist')

        return None
