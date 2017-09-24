import packer

PACKERFILE = "ubuntu_linux_12.04_server_sp0_eng_64bit.json"

def test_packer():
    """Test Packer methods
    """
    only = ['virtualbox-iso']
    pi = packer.Packer(PACKERFILE, only=only)
    pi.version()
    pi.validate()
    pi.build(force=True)

test_packer()
