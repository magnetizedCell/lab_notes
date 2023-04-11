import os
import shutil
import subprocess

APT_PACKAGES = """ca-certificates \
    curl \
    gnupg \
    lsb-release \
    build-essential \
    uuid-dev \
    libgpgme11-dev \
    squashfs-tools \
    libseccomp-dev \
    pkg-config \
    nfs-common \
    slurm-wlm munge \
    libmunge-dev \
    uidmap \
    squashfuse \
    fuse2fs \
    fuse-overlayfs \
    fakeroot \
    cryptsetup \
    wget git \
    """

CONTROLLER = """200.0.0.255 controller"""
NFS_SETTING = """200.0.0.255:/projects /projects nfs4 rw,relatime,vers=4.2,proto=tcp,timeo=6000 0 0
200.0.0.255:/archive /archive nfs4 rw,relatime,vers=4.2,proto=tcp,timeo=6000 0 0
"""

def run(operation):
    print(operation)
    res = subprocess.run(operation, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"{operation} failed with message {res.stderr}")
        print('Press Y to continue else abort.')
        input_ = input()
        if input_ != 'Y':
            raise ValueError("Aborting.")
    else:
        print(res.stdout)


def add_to_file(file, string, check_duplicate=True):
    with open(file, 'a+') as f:
        if check_duplicate:
            content = f.read()
            for line in string.splitlines():
                if line in content:
                    print(f'{line} already in the target file.')
                    print('Press Y to continue else skip.')
                    input_ = input()
                    if input_ != 'Y':
                        pass
                    f.write(line+'\n')


def main():
    add_to_file('/etc/hosts', CONTROLLER)
    run("apt update")
    run(f"apt install  -y {APT_PACKAGES}")
    
    # NFS setting
    os.makedirs("/archive", exist_ok=True)
    os.makedirs("/projects", exist_ok=True)
    add_to_file("/etc/fstab", NFS_SETTING)
    run(f"mount -a")

    # munge and slurm setting
    run("cp /projects/setting/munge.key /etc/munge/")
    run("chmod 400 /etc/munge/munge.key")
    run("cp /projects/setting/*.conf /etc/slurm/")

    # apptainer setting
    run("snap install go --classic")
    os.chdir('/tmp')
    run("git clone https://github.com/apptainer/apptainer.git")
    os.chdir("apptainer")
    run("./mconfig")
    os.chdir("builddir")
    run("make")
    run("make install")


if __name__ == '__main__':
    main()