#from vmimage import *

class VMImage(object):
    def __init__(self, vm):
        #print('VMImage class is defined')
        self.user = vm['user']
        self.password = vm['pass']
        self.os = vm['os']
        self.arch = vm['arch']
        self.iso = vm['iso']
        self.language = vm['language']
        self.displayname = "{0} {1}-bit {2}".format(self.os, self.arch,
                                                    self.language).title()
        print(self.displayname)
        self.short_name = "{0}".format('_'.join([sn[:3]
                                        for sn in self.displayname.split(' ')]).
                                        lower().replace('-',''))
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
