import argparse
import logging
import os
#from vmimage.vmimage import *
from vmimage import buildvm
__author__ = 'Sandeep Koli'

def get_args():
    '''This function parses and return arguments passed in'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(description='Script retrieves schedules from a given server', add_help=True,
                                    formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=50))

    # Add arguments
    parser.add_argument('-i', '--image',
                        required=False,
                        type=str,
                        default='vm',
                        help='Vitual Machine image type, e.g. vm, vagrant',
                        metavar='\b')
    parser.add_argument('-hv','--hypervisor',
                        required=False,
                        type=str,
                        default='virtualbox',
                        help='Hypervisor, e.g. vmware, virtualbox, hyperv',
                        metavar='\b')
    parser.add_argument('-u', '--user',
                        required=False,
                        type=str,
                        default='vmuser',
                        help='User of VM',
                        metavar='\b')
    parser.add_argument('-p', '--pass',
                        required=False,
                        type=str,
                        default='vmpass',
                        help='Password for VM',
                        metavar='\b')
    parser.add_argument('-o', '--os',
                        required=True,
                        type=str,
                        default=None,
                        help='OS of VM, e.g. windows, linux',
                        metavar='\b')
    parser.add_argument('-a', '--arch',
                        required=True,
                        type=str,
                        default=None,
                        help='Architecture of VM, e.g. 32, 64',
                        metavar='\b')
    parser.add_argument('-iso', '--iso',
                        required=True,
                        type=str,
                        default=None,
                        help='ISO path to installed in VM',
                        metavar='\b')
    # Array for all arguments passed to script
    args = vars(parser.parse_args())

    return args #image, hypervisor, vmuser, vmpass, os, arch, iso

def main():
    logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] (%(module)s:%(lineno)d) %(message)s", )
    # Run get_args()
    # get_args()
    DEFAULT_HYPERVISOR = "virtualbox"
    # Match return values from get_arguments()
    # and assign to their respective variables
    arg_dict = get_args()
    #print(arg_dict)

    # Print the values
    '''
    logging.info("Image type: %s" % image)
    logging.info("Hypervisor: %s" % hypervisor)
    logging.info("VM user: %s" % vmuser)
    logging.info("VM password: %s" % vmpass)
    logging.info("VM OS: %s" % vmos)
    logging.info("VM Architecture: %s" % vmarch)
    logging.info("VM ISO: %s" % vmiso)
    '''

    vm = buildvm.BuildVM(arg_dict)
    vm.Build()

    #print(executable_in_path('packer'))
if __name__ == '__main__':
    main()
