#!/usr/bin/env python

# Built-in modules
import argparse
import logging
import sys

# Local modules
import vmtask

def parse_input():
    parser = argparse.ArgumentParser(description="Utility to carry out tasks on a running virtual machine")

    """
    list_tasks = {'mount' : 'Mount an already existing block format it and mount it'}
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
    group_mount.add_argument('--format', metavar='<filesystem type>', required=False, dest='format', choices= ['ext2', 'ext3', 'ext4'], help='filesystem type to format the block with')
    group_mount.add_argument('--mountpoint', metavar='<mountpoint>', required=False, dest='mountpoint', help='directory path to mount at')

    group_mount = parser.add_argument_group('Attaching shared storage options')
    group_mount.add_argument('--osuser', required=False, dest='osuser', help='OpenStack user name')
    group_mount.add_argument('--cinder-id', dest='cinder_id', help='volume ID of the Cinder volume to be attached')
    group_mount.add_argument('--instance-id', dest='instance_id', help='instance ID to attach the volume to')

    return parser.parse_args()

def main():
    argv = parse_input()

    # Create a new task instance
    task = vmtask.Task()

    # Send credential info to task module
    task.set_credentials(argv.host, argv.user, argv.key, argv.windows) # Check for error

    # Now call the specific task
    if argv.osuser or argv.cinder_id or argv.instance_id:
        ret = task.do_task(vmtask.TASKTYPE.TASK_SHARED_STORAGE, argv.osuser, argv.cinder_id, argv.instance_id)
        if ret == -1:
            logging.critical("Some error")

    if argv.format or argv.mountpoint:
        ret = task.do_task(vmtask.TASKTYPE.TASK_FORMAT_MOUNT, argv.format, argv.mountpoint)
        if ret == -1:
            logging.critical("Some error")


if __name__ == "__main__":
    main()
