from .vmimage import *
import json

class VMLinux(VMImage):
    def __init__(self, vm):
        super().__init__(vm)

    def answerfile(self):
        _input_template_file_deb = os.path.join(PACKERFILE_TEMPLATES_DIR, 'linux',
                        'debian_based.cfg')
        self.answerfile = os.path.join(INPUT_ARTIFACTS_DIR, 'linux',
                        self.vm_dir, 'preseed.cfg')

        if not os.path.exists(os.path.dirname(self.answerfile)):
            os.makedirs(os.path.dirname(_output_answerfile))

        shutil.copyfile(_input_template_file_deb, self.answerfile)
        helper.SearchReplaceInFile(self.answerfile, '%Var.UserName%', self.user)
        helper.SearchReplaceInFile(self.answerfile, '%Var.Password%', self.password)

    def packerfile(self):
        _input_packerfile = os.path.join(PACKERFILE_TEMPLATES_DIR, 'linux',
                        'linux_packer.json')
        self.vm_packerfile = os.path.join(INPUT_ARTIFACTS_DIR, 'linux',
                        self.vm_dir, "packerfile.json")

        if not os.path.exists(os.path.dirname(self.vm_packerfile)):
            os.makedirs(os.path.dirname(self.vm_packerfile))

        try:
            with open(_input_packerfile) as data_file:
                data = json.load(data_file)
        except Exception as e:
            logging.error("error in opening packer template json file")
            logging.error(str(e.message))

        assert isinstance(data, object)
        data['variables']['guestos'] = "Ubuntu" #utils.get_guestos(self.image_version, self.image_architecture, self.image_provider)
        data['variables']['ramsize'] = str(self.ram)
        data['variables']['disksize'] = str(self.disk)
        data['variables']['image_username'] = self.user
        data['variables']['image_password'] = self.password
        data['variables']['displayname'] = self.displayname
        data['variables']['iso_path'] = self.iso.replace("\\", "/")
        data['variables']['answerfile'] = self.answerfile.replace("\\", "/")
        data['variables']['indir'] = self.indir.replace('\\', '/')
        data['variables']['outdir'] = self.outdir.replace('\\', '/')
        with open(self.vm_packerfile, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    def Build(self):
        #print("build linux " + self.vm['image'])
        self.buildimage()
