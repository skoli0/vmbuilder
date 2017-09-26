from .vmimage import *
from packer.packer import *

class VMLinux(VMImage):
    def __init__(self, vm):
        super().__init__(vm)
        #self.vm = vm

    def answerfile(self):
        _input_template_file_deb = os.path.join(PACKERFILE_TEMPLATES_DIR, 'linux',
                        'debian_based.cfg')
        _output_answerfile_deb = os.path.join(INPUT_ARTIFACTS_DIR, 'linux',
                        self.vm_dir, 'preseed.cfg')

        if not os.path.exists(os.path.dirname(_output_answerfile_deb)):
            os.makedirs(os.path.dirname(_output_answerfile))

        shutil.copyfile(_input_template_file_deb, _output_answerfile_deb)

        _input_template_file_rpm = os.path.join(PACKERFILE_TEMPLATES_DIR, 'linux',
                        'rhel_based.cfg')
        _output_answerfile_rpm = os.path.join(INPUT_ARTIFACTS_DIR, 'linux',
                        self.vm_dir, 'ks.cfg')

        shutil.copyfile(_input_template_file_rpm, _output_answerfile_rpm)

    def packerfile(self):
        _input_packerfile = os.path.join(PACKERFILE_TEMPLATES_DIR, 'linux',
                        'linux_packer.json')
        self.vm_packerfile = os.path.join(INPUT_ARTIFACTS_DIR, 'linux',
                        self.vm_dir, "packerfile.json")

        if not os.path.exists(os.path.dirname(self.vm_packerfile)):
            os.makedirs(os.path.dirname(self.vm_packerfile))

        shutil.copyfile(_input_packerfile, self.vm_packerfile)

    def Build(self):
        #print("build linux " + self.vm['image'])
        self.buildimage()
