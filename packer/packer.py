import sys
sys.path.append("..")
from helper.helper import *

# inspiration of this Packer interface for Python is taken from https://github.com/nir0s/python-packer.git
DEFAULT_TEMPLATES_PATH = "templates"
DEFAULT_SCRIPTS_PATH = "scripts"

class Packer(object):
    """
    A packer client.
    """

    def __init__(self, packerfile, exc=None, only=None):
        """
        :param string packerfile: Path to Packer template file
        :param list exc: List of builders to exclude
        :param list only: List of builders to include
        :param string exec_path: Path to Packer executable
        """
        exec_path = helper.executable_in_path('packer')
        if exec_path == None:
            raise OSError('packer binary not found in this system. please donwload and install it.')

        self.packer_cmd = ""

        self.packerfile = self._validate_argtype(packerfile, str)
        if not os.path.isfile(self.packerfile):
            raise OSError('packerfile not found at path: {0}'.format(self.packerfile))
        self.exc = self._validate_argtype(exc or [], list)
        self.only = self._validate_argtype(only or [], list)

        self.packerfile = '%s'%self.packerfile

        self.packer = '%s'%exec_path

    def build(self, debug=False, force=False):
        """Executes a `packer build`

        :param bool parallel: Run builders in parallel
        :param bool debug: Run in debug mode
        :param bool force: Force artifact output even if exists
        """
        self.packer_cmd = self.packer
        self._add_opt("build")

        #self._add_opt('-parallel=true' if parallel else None)
        self._add_opt('-debug' if debug else None)
        self._add_opt('-force' if force else None)
        self._append_base_arguments()
        self._add_opt(self.packerfile)
        print(self.packer_cmd)

        try:
            build = helper.run(self.packer_cmd)
            if build == 0:
                return True
        except subprocess.CalledProcessError as ex:
            logging.info(ex.message)

        return False

    def validate(self, syntax_only=False, only='virtualbox'):
        """Validates a Packer Template file (`packer validate`)

        If the validation failed, an `pbs. exception will be raised.
        :param bool syntax_only: Whether to validate the syntax only
        without validating the configuration itself.
        """
        self.packer_cmd = self.packer
        self._add_opt("validate")

        self._add_opt('-syntax-only' if syntax_only else None)
        self._append_base_arguments()
        #self._add_opt(self.only)
        self._add_opt(self.packerfile)
        print(self.packer_cmd)

        try:
            validation = helper.run(self.packer_cmd)
            if validation == 0:
                return True
        except subprocess.CalledProcessError as ex:
            logging.info(ex.message)

        return False

    def version(self):
        """Returns Packer's version number (`packer version`)
        As of v0.7.5, the format shows when running `packer version`
        is: Packer vX.Y.Z. This method will only returns the number, without
        the `packer v` prefix so that you don't have to parse the version
        yourself.
        """
        self.packer_cmd = self.packer
        self._add_opt("version")
        try:
            version = helper.run(self.packer_cmd)
            #print(self.packer_cmd)
            #version = "1.1.0"
            if version == 0:
                return True
        except subprocess.CalledProcessError as ex:
            logging.info(ex.message)

        return False

    def _add_opt(self, option):
        """Append given optional parameters to the command
        :param option: Optional parameter to be appended
        :return: Returns the final command with parameters appended
        """
        if option:
            self.packer_cmd = self.packer_cmd + " " + option

    def _validate_argtype(self, arg, argtype):
        """Validates given argument against its type
        :param arg: Argument
        :param argtype: Argument type
        :return: Result argument
        """
        if not isinstance(arg, argtype):
            raise PackerException('{0} argument must be of type {1}'.format(
                arg, argtype))
        return arg

    def _append_base_arguments(self):
        """Appends base arguments to packer commands.

        -except, -only, -var and -var-file are appeneded to almost
        all subcommands in packer. As such this can be called to add
        these flags to the subcommand.
        """
        if self.exc and self.only:
            raise PackerException('Cannot provide both "except" and "only"')
        elif self.exc:
            self._add_opt('-except={0}'.format(self._join_comma(self.exc)))
        elif self.only:
            self._add_opt('-only={0}'.format(self._join_comma(self.only)))

    def _join_comma(self, lst):
        """Returns a comma delimited string from a list

        :param lst: List to which comma to be added
        :return: A comma delimited list
        """
        return str(','.join(lst))

class PackerException(Exception):
    """Custom Packer exception
    """
    pass
