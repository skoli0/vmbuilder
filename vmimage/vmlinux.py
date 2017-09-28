from .vmimage import *
import json

boot_cmd = {
    "ubuntu": [
        "<enter><wait><f6><esc><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs>",
        "<bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs>",
        "<bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs><bs>",
        "<bs><bs><bs><bs><bs><bs><bs><bs>",
        "/install/vmlinuz ",
        "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg<wait> ",
        "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ",
        "hostname={{.Name}} ",
        "fb=false debconf/frontend=noninteractive ",
        "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ",
        "keyboard-configuration/variant=USA console-setup/ask_detect=false ",
        "initrd=/install/initrd.gz -- <enter>"
    ],
    "red": ["<tab> text ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/ks.cfg hostname={{.Name}}<enter><wait>"],
    "centos": ["<tab> text ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/ks.cfg hostname={{.Name}}<enter><wait>"],
    "fedora": ["<tab> text ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/ks.cfg hostname={{.Name}}<enter><wait>"]
}

class VMLinux(VMImage):
    def __init__(self, vm):
        super().__init__(vm, "linux")

    def answerfile(self):
        _input_template_file_deb = os.path.join(PACKERFILE_TEMPLATES_DIR, 'linux',
                        'debian_based.cfg')
        self.answerfile = os.path.join(self.vmindir, 'preseed.cfg')

        if not os.path.exists(os.path.dirname(self.answerfile)):
            os.makedirs(os.path.dirname(self.answerfile))

        shutil.copyfile(_input_template_file_deb, self.answerfile)
        helper.SearchReplaceInFile(self.answerfile, '%Var.UserName%', self.user)
        helper.SearchReplaceInFile(self.answerfile, '%Var.Password%', self.password)

    def packerfile(self):
        _input_packerfile = os.path.join(PACKERFILE_TEMPLATES_DIR, 'linux',
                        'linux_packer.json')
        self.vm_packerfile = os.path.join(self.vmindir, "packerfile.json")

        if not os.path.exists(os.path.dirname(self.vm_packerfile)):
            os.makedirs(os.path.dirname(self.vm_packerfile))

        try:
            with open(_input_packerfile) as data_file:
                data = json.load(data_file)
        except Exception as e:
            logging.error("error in opening packer template json file")
            logging.error(str(e.message))

        assert isinstance(data, object)

        data['variables']['vm_name'] = self.vm_dir
        data['variables']['guestos'] = "Ubuntu" #utils.get_guestos(self.vm_version, self.vm_architecture, self.vm_provider)
        data['variables']['ramsize'] = str(self.ram)
        data['variables']['disksize'] = str(self.disk)
        data['variables']['vm_username'] = self.user
        data['variables']['vm_password'] = self.password
        data['variables']['displayname'] = self.displayname
        data['variables']['iso_path'] = self.iso.replace("\\", "/")
        data['variables']['answerfile'] = os.path.basename(self.answerfile)
        data['variables']['indir'] = self.vmindir.replace('\\', '/')
        data['variables']['outdir'] = self.vmoutdir.replace('\\', '/')

        for builder in data['builders']:
            builder['boot_command'] = boot_cmd['ubuntu']

        with open(self.vm_packerfile, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    def Build(self):
        #print("build linux " + self.vm['image'])
        self.buildimage()
