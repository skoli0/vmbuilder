from .vmimage import *

class VMWindows(VMImage):
    def __init__(self, vm):
        super().__init__(vm, "windows")
        #self.vm = vm

    def answerfile(self):
        self._sif, self._xml = self.get_answerfile(self.osfamily)
        print(self._sif, self._xml)
        shutil.copy2(self._sif, self.vmindir)
        shutil.copy2(self._xml, self.vmindir)

    def packerfile(self):
        _input_packerfile = self.get_packerfile()

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
        data['variables']['xml_answerfile'] = os.path.basename(self._xml)
        data['variables']['indir'] = self.vmindir.replace('\\', '/')
        data['variables']['outdir'] = self.vmoutdir.replace('\\', '/')

        with open(self.vm_packerfile, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    def Build(self):
        #print("build linux " + self.vm['image'])
        self.buildimage()
