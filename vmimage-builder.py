import argparse
import logging

__author__ = 'Sandeep Koli'

def get_args():
    '''This function parses and return arguments passed in'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(description='Script retrieves schedules from a given server', formatter_class=argparse.MetavarTypeHelpFormatter)
    # Add arguments
    parser.add_argument('-i', '--image', type=str, help='VM image type, e.g. vm, vagrant', required=True, metavar='\b')
    parser.add_argument('-hv', '--hypervisor', type=str, help='Hypervisor, e.g. vmware, virtualbox, hyperv', required=True, metavar='\b')
    parser.add_argument('-u', '--user', type=str, help='User of VM', required=False, default="vmuser", metavar='\b')
    parser.add_argument('-p', '--password', type=str, help='Password for VM', required=False, default="vmpass", metavar='\b')
    parser.add_argument('-o', '--os', type=str, help='OS of VM', required=True, default=None, metavar='\b')
    parser.add_argument('-a', '--arch', type=str, help='Architecture of VM', required=True, default=None, metavar='\b')
    parser.add_argument('-iso', '--iso', type=str, help='ISO path to installed in VM', required=True, default=None, metavar='\b')
    #parser.add_argument('-h', '--help', action='help', help='Show this help message and exit.')
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    image = args.image
    hypervisor = args.hypervisor
    vmuser = args.user
    vmpass = args.password
    os = args.os
    arch = args.arch
    iso = args.iso
    # Return all variable values
    return image, hypervisor, vmuser, vmpass, os, arch, iso

def main():
    logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] (%(module)s:%(lineno)d) %(message)s", )
    # Run get_args()
    # get_args()
    DEFAULT_HYPERVISOR = "virtualbox"
    # Match return values from get_arguments()
    # and assign to their respective variables
    image, hypervisor, vmuser, vmpass, vmos, vmarch, vmiso = get_args()

    # Print the values
    '''
    print("Image type: %s" % image)
    print("Provider: %s" % hypervisor)
    print("VM user: %s" % vmuser)
    print("VM password: %s" % vmpass)
    print("VM OS: %s" % vmos)
    print("VM Architecture: %s" % vmarch)
    print("VM ISO: %s" % vmiso)
    '''
    logging.info("Image type: %s" % image)
    logging.info("Provider: %s" % hypervisor)
    logging.info("VM user: %s" % vmuser)
    logging.info("VM password: %s" % vmpass)
    logging.info("VM OS: %s" % vmos)
    logging.info("VM Architecture: %s" % vmarch)
    logging.info("VM ISO: %s" % vmiso)

if __name__ == '__main__':
    main()
