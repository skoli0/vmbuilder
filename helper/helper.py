import re
import os, sys
import json
import csv
import ctypes
import logging
import datetime
import fileinput
import subprocess
import xml.etree.ElementTree as etree

DEFAULT_HELPER_PATH = "helper"

class Logger(object):
    def __init__(self):
        """Init method

        """
        self.terminal = sys.stdout
        self.log = open("image-gen-logfile.log", "a")

    def write(self, message):
        """Writes a log message

        :param message:
        :return:
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S - ')
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        """Flushes a log message

        :return:
        """
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        pass

class helper(object):
    @staticmethod
    def executable_in_path(executable):
        '''Returns the full path to an executable according to PATH,
        otherwise None.'''
        path = os.environ.get('PATH')
        if not path:
            print >> sys.stderr, "Warning: No PATH could be searched"
        paths = path.split(':')
        for path in paths:
            fullpath = os.path.join(path, executable)
            if os.path.isfile(fullpath) and os.access(fullpath, os.X_OK):
                return fullpath
        return None

    @staticmethod
    def validate_argtype(arg, argtype):
        """Validates argument against given type

        :param arg:
        :param argtype:
        :return:
        """
        if not isinstance(arg, argtype):
            raise HelperException('{0} argument must be of type {1}'.format(
                arg, argtype))
        return arg

    @staticmethod
    def get_guestos(os_string, os_arch, image_provider):
        """Returns guest os type for a specific provider

        :param os_string:
        :param os_arch:
        :param image_provider:
        :return:
        """

        if "linux" in os_string.lower():
            guestos = re.sub(r'\W+', ' ', re.sub(r'\d+', ' ', os_string)).strip()
        if "windows" in os_string.lower():
            guestos = os_string

        if os_arch == '64':
            guestos = guestos + "_" + str(os_arch)

        guestos = guestos.replace(" ", "_")


        data = ""
        try:
            guest_os_file = os.path.join(DEFAULT_HELPER_PATH, (image_provider.lower() + '-guestos.json'))
            with open(guest_os_file) as data_file:
                data = json.load(data_file)
        except (OSError, IOError) as ex:
            print("error in opening packer template json file")
            logging.error(ex.message)
            print(str(ex.message))

        assert isinstance(data, object)

        if guestos in data:
            return data[guestos]
        elif "windows" in guestos.lower():
            if os_arch == 32:
                return data['Windows']
            else:
                return data['Windows_64']
        elif "linux" in guestos.lower():
            if os_arch == 32:
                return data['Linux']
            else:
                return data['Linux_64']
    @staticmethod
    def run(cmd):

        """Runs a command
        :param cmd: Command
        :return: Execution status
        """

        try:
            '''
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in iter(p.stdout.readline, ''):
                print(line)
            retval = p.wait()
            return retval
            '''
            p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
            for line in iter(p.stdout.readline, b''):
                print(line.rstrip().decode('utf-8')),
            p.stdout.close()
            p.wait()
            #print(cmd)
            #p = subprocess.run(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #print('returncode:', p.returncode)
            #print('{}'.format(p.stdout.decode('utf-8')))
        except (subprocess.CalledProcessError, KeyboardInterrupt) as e:
            print("Received keyboard interrupt, terminating the build process...")

            '''
            """kill function for Win32"""
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.OpenProcess(1, 0, p.pid)
            return (0 != kernel32.TerminateProcess(handle, 0))

            logging.error("Error occured while running command {0}, Error: {1}".format(cmd, e.message))
            raise subprocess.CalledProcessError
            '''

    @staticmethod
    def SearchReplaceInFile(file, searchpattern, replacewith):
        """

        :param file:
        :param searchpattern:
        :param replacewith:
        :return:
        """

        for line in fileinput.input(file, inplace=1):
            if searchpattern in line:
                line = line.replace(searchpattern, replacewith)
            sys.stdout.write(line)
        fileinput.close()

    @staticmethod
    def get_productkey(_dbms_query):
        """

        :param _dbms_query:
        :return:
        """
        return " "

class HelperException(Exception):
    """Custom helper exception
    """
    pass
