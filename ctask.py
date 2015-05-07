# coding: utf-8

# Built-in modules
import logging
from subprocess import PIPE
import subprocess
import re
import string

# Third-party modules
import paramiko
import cinderclient.v1.client as cclient

# Local modules
import cmapper as mapper

# Enum for VM type
class TASKTYPE:
    TASK_MOUNT = 1
    TASK_SHARED_STORAGE = 2
    TASK_OTHERS = 3

class Task():

    def __init__(self):
        self.host = ''
        self.user = ''
        self.keypath = ''
        self.ssh = ''

    def set_credentials(self, host, user, key, isWindows):
        self.host = host
        self.user = user
        self.keypath = key
        self.isWindows = isWindows

    def _do_login(self):

        if not self.isWindows:
            # TODO: Handle errors at each step
            # Create a new SSHClient object from Paramiko
            self.ssh = paramiko.SSHClient()

            # Prompt for missing host key in known_hosts set to auto
            # TODO: Give an option to not do this?
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Read key from private key file
            # TODO: Ability to add different sources of keys
            key = paramiko.RSAKey.from_private_key_file(self.keypath)

            # Attempt to connect to SSH
            # TODO: Key sources!
            # TODO: Check for error
            self.ssh.connect(hostname = str(self.host), username = str(self.user), pkey = key)

            return True

        else:
            # For now
            logging.error("Windows-based virtual machines not supported")

    def do_task(self, task_type, *args):
	
        if not self.ssh:
            # Perform login to the virtual machine
            ret = self._do_login()
            if ret == -1:
                logging.critical("Some SSH error")
	
        # TODO: More sanity checks?

        if task_type == TASKTYPE.TASK_MOUNT:
		print "Inside Task Mount"
		self._do_format_and_mount(*args)

        elif task_type == TASKTYPE.TASK_SHARED_STORAGE:
            self._do_attach_shared_storage(*args)

        else:
            print "No other tasks defined"  # TODO: Better error handling

        # Disconnect the SSH session
        ret = self._do_terminate()


    def _onlyascii(self, char):

        if ord(char) < 1 or ord(char) > 127: return ''
        else: return char

    def _do_format_and_mount(self, filesystem, mountpoint, size,cinder_id):

        #self._locate_block_format_and_mount(filesystem, mountpoint,size)

        #stdin, stdout, stderr = self.ssh.exec_command("pwd; ls -al")
        #print stdout.read()
        #print stderr.read()

        # dummy
        cc = cclient.Client('puser6may', 'password', 'project6may', 'http://localhost:5000/v2.0', service_type="volume")
        print "object created", cinder_id
	list_cinder = cc.volumes.get(cinder_id)._info["attachments"]
	dev_name = list_cinder[0]["device"]
	
	dev_name = "/dev/vdb"
	cmd_format = "sudo mkfs -t " + filesystem + " " + dev_name
	chan = self.ssh.get_transport().open_session()

	chan.get_pty()
	stdin, stdout, stderr = self.ssh.exec_command(cmd_format)
	print stdout.read()
	print stderr.read()

	cmd_mount = "sudo mkdir -p " + mountpoint
	stdin, stdout, stderr = self.ssh.exec_command(cmd_mount)
	cmd_mount = "sudo mount " + dev_name + " " + mountpoint
	stdin, stdout, stderr = self.ssh.exec_command(cmd_mount)
	print stdout.read()
	print stderr.read()
	print "output"
	return

    def _do_attach_shared_storage(self, user_id, cinder_id, instance_id):

        # dummy
        if not mapper.Mapper.check_exist_user_cinder(user_id, cinder_id):
            print "User not authorized"

        else:
            print "User authorized"

    def _locate_block_format_and_mount(self, filesystem, mountpoint, size):

        #print filesystem, mountpoint, force

        stdin, stdout, stderr = self.ssh.exec_command("sudo lsblk -b --output NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT")

        cmd = stdout.read()
        cmd = filter(self._onlyascii, cmd)

        #cmd =  cmd.replace('├─','')     # Special characters have been removed
        #cmd =  cmd.replace('└─','')
        data = re.split('[\n]',cmd)     # Reading the command output line by line
        for i in range(len(data)):
            data[i]=re.sub("\s\s+" , " ", data[i])  # Replacing multiple spaces in the line with a single space
        

        info_new = []       # List to store the device names ,type (disk/part) and volume size of those devices which are neither formatted 
                            # nor mounted. Index [0,3,6....] stores the device name & index [1,4,7....] store the device size & index [2.5.8..]
                            # store the device type
        info_fs = []        # List to store the device name,volume size,type and file system of those devices which are formatted but not 
                            # mounted. Index [0,4,8...] stores the device name index [1,5,9,...] store the device size, index [2,6,10,..] store 
                            # the type and index [3,7,11,.....] store the file system

        for i in range(len(data)):
            if i>1:         # This has been done assuming that the first entry would be the heading of the columns and the second entry
                            # would be the first primary disk containing the OS and further partitions
                finaldata = re.split(' ',data[i])   # Each line is split on the basis of spaces
                
                if len(finaldata)==4:
                    info_new.append(finaldata[0])
                    info_new.append(finaldata[1])
                    info_new.append(finaldata[2])


                elif (len(finaldata)==5 and finaldata[4]==""):
                    info_fs.append(finaldata[0])
                    info_fs.append(finaldata[1])
                    info_fs.append(finaldata[2])
                    info_fs.append(finaldata[3])

        if filesystem:
            i = 1
            while i < len(info_new):
                if info_new[i] == size:
                    dev_name = "/dev/" + info_new[i-1]
                    break
                i = i + 3
            # TODO: safe dev_name
            # TODO: Check for already existing mountpoint
            cmd_format = "sudo mkfs -t " + filesystem + " " + dev_name
            stdin, stdout, stderr = self.ssh.exec_command(cmd_format)
            print stdout.read()
            print stderr.read()
            cmd_mount = "sudo mkdir -p " + mountpoint
            #stdin, stdout, stderr = self.ssh.exec_command(cmd_mount)
            cmd_mount = "sudo mount " + dev_name + " " + mountpoint
            #stdin, stdout, stderr = self.ssh.exec_command(cmd_mount)
            #print stdout.read()
            #print stderr.read()
            return

        else:
            i = 1
            while i < len(info_fs):
                if info_fs[i] == size:
                    dev_name = "/dev/" + info_fs[i-1]
                    filesystem = info_fs[i+2]
                    break
                i = i + 4
            # TODO: safe dev_name
            # TODO: Check for already existing mountpoint
            cmd_mount = "sudo mkdir -p " + mountpoint
            #stdin, stdout, stderr = self.ssh.exec_command(cmd_mount)
            cmd_mount = "sudo mount " + dev_name + " " + mountpoint
            #stdin, stdout, stderr = self.ssh.exec_command(cmd_mount)
            #print stdout.read()
            #print stderr.read()
            return

    def _do_terminate(self):
        self.ssh.close()
