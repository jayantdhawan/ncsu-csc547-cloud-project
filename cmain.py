 #!/usr/bin/python3.4

# Import all dependencies
import argparse
import logging
import sys
import ctask as ctask

class ConfigParser():

    def parse_input(self):
        parser = argparse.ArgumentParser(description="Utility to carry out tasks on a running virtual machine")

        """
        list_of_tasks = {'mount':'mount an already existing block or find a cinder block attached to the instance, format it and mount it'}
        subparser = parser.add_subparsers(dest='task', help = "commands based on the list of tasks")
        task_subparsers = []
        for i in list_of_tasks.keys():
            task_subparsers.append(subparser.add_parser(i, help=list_of_tasks[i]))
            if i=='mount':
                task_subparsers[len(task_subparsers)-1].add_argument('-a', action="store_true", dest="a", default="False", help="This is true if you want to retrieve an already existing cinder block")
                task_subparsers[len(task_subparsers)-1].add_argument('--file-system', action="store", dest="fs", help="Type of file system the block needs to be formatted in")
                task_subparsers[len(task_subparsers)-1].add_argument('--mount', action="store", dest="mount", help="Mount point of the cinder block")
                break
        """

        group_mount = parser.add_argument_group('Options')
        group_mount.add_argument('--host', required=True, action="store", dest="host", help="The host name or IP address of the VM instance")
        group_mount.add_argument('--user', required=True, action="store", dest="user", help="Username to login with")
        group_mount.add_argument('--key', required=True, action="store", dest="key", help="Path of the key")
        group_mount.add_argument('--windows', required=False, action="store_true", default=False, dest="windows", help="flag indicating whether the VM is Windows-based; otherwise it is assumed to be Linux-based")

        group_mount = parser.add_argument_group('Format and mount options')
        group_mount.add_argument('--format', metavar='<type>', required=False, dest='format', choices= ['ext2', 'ext3', 'ext4'], help='filesystem type to format the block with')
        group_mount.add_argument('--mountpoint', metavar='<mountpoint>', dest='mountpoint', help='directory path to mount at')
        group_mount.add_argument('--size', metavar='<size in bytes>', dest='size', help='size of the block to be found')

        group_mount = parser.add_argument_group('Attaching shared storage options')
        group_mount.add_argument('--osuser', required=False, dest='osuser', help='OpenStack user name')
        group_mount.add_argument('--cinder-id', dest='cinder_id', help='volume ID of the Cinder volume to be attached')
        group_mount.add_argument('--instance-id', dest='instance_id', help='instance ID to attach the volume to')

        return parser.parse_args()

def main():
    test = ConfigParser()
    cinput = test.parse_input()

    # Create a new task instance
    task = ctask.Task()

    # Send credential info to task module
    task.set_credentials(cinput.host, cinput.user, cinput.key, cinput.windows) # Check for error

    # Perform login to the virtual machine
    ret = task.do_login()
    if ret == -1:
        logging.critical("Some SSH error")

    # Now call the specific task
    if cinput.format or cinput.mountpoint:
        ret = task.do_task(ctask.TASKTYPE.TASK_MOUNT, cinput.format, cinput.mountpoint, cinput.size)
        if ret == -1:
            logging.critical("Some error")
    elif cinput.osuser:
        ret = task.do_task(ctask.TASKTYPE.TASK_SHARED_STORAGE, cinput.osuser, cinput.cinder_id, cinput.instance_id)
        if ret == -1:
            logging.critical("Some error")

    # Disconnect the SSH session
    ret = task.do_terminate()


if __name__ == "__main__":
    main()
