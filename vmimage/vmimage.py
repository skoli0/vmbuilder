import os
import shutil
from packer.packer import *

PACKERFILE_TEMPLATES_DIR = "templates"
INPUT_ARTIFACTS_DIR = "input-artifacts"
OUTPUT_ARTIFACTS_DIR = "output-artifacts"

class VMImage(object):
    def __init__(self, vm):
        #print('VMImage class is defined')
        self.user = vm['user']
        self.password = vm['pass']
        self.os = vm['os']
        self.arch = vm['arch']
        self.iso = vm['iso']
        self.hypervisor = vm['hypervisor']
        self.ram = vm['ram']
        self.disk = int(vm['disk']) * 1024
        self.language = vm['language']
        self.displayname = "{0} {1}-bit {2}".format(self.os, self.arch,
                                                    self.language).title()
        print(self.displayname)
        self.short_name = "{0}".format('_'.join([sn[:3]
                                        for sn in self.displayname.split(' ')]).
                                        lower().replace('-',''))
        self.vm_dir = self.displayname.replace(' ', '_')
        self.indir = os.path.join(INPUT_ARTIFACTS_DIR, self.hypervisor, self.vm_dir)
        print(self.indir)
        self.outdir = os.path.join(OUTPUT_ARTIFACTS_DIR, self.hypervisor, self.vm_dir)

        print(self.short_name)
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
        self.build()
        self.cleanup()
