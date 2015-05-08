#!/usr/bin/env python

# Built-in modules
import argparse
import logging
import sys

# Local modules
import vmtask

def parse_input():
    parser = argparse.ArgumentParser(description="Utility to carry out tasks on a running virtual machine")

    subparser = parser.add_subparsers(dest='task', metavar="<subcommand>")

    parser_mount = subparser.add_parser('mount', help="Format (optional) and mount a device")
    parser_mount.add_argument('--host', required=True, action="store", dest="host", help="Host name or IP address of the VM instance")
    parser_mount.add_argument('--user', required=True, action="store", dest="user", help="Alias for the user account on VM's host OS")
    parser_mount.add_argument('--keyfile', required=False, action="store", dest="key", help="(Optional) Path of the file containing private key; if omitted, it will be fetched from the database")
    parser_mount.add_argument('--windows', required=False, action="store_true", default=False, dest="windows", help="(Optional) Flag indicating whether the VM is Windows-based; if omitted it is assumed to be Linux-based")
    parser_mount.add_argument('--cinder-id', metavar='<cinder-id>', required=True, dest='cinder_id', help='Cinder block ID needed to fetch device file name')
    parser_mount.add_argument('--format', metavar='<filesystem type>', required=False, dest='format', choices= ['ext2', 'ext3', 'ext4'], help='(Optional) Filesystem type to format the block with; if omitted, the device is assumed to be already formatted, and only mounted')
    parser_mount.add_argument('--mountpoint', metavar='<mountpoint>', required=True, dest='mountpoint', help='Directory path to mount at; if the path does not exist, it will be created')    
    parser_mount.add_argument('--os-user', metavar='<OS_USERNAME>', required=False, dest='os_user', help='(Optional) Alias for the OpenStack user for connecting to the Cinder API service; can be omitted with setting env variable OS_USERNAME')
    parser_mount.add_argument('--os-password', metavar='<OS_PASSWORD>', required=False, dest='os_password', help='(Optional) Password for the OpenStack user; can be omitted with setting env variable OS_PASSWORD')
    parser_mount.add_argument('--os-tenant-name', metavar='<OS_TENANT_NAME>', required=False, dest='os_tenant_name', help='(Optional) OpenStack tenant (project) name; can be omitted with setting env variable OS_TENANT_NAME')
    parser_mount.add_argument('--os-auth-url', metavar='<OS_AUTH_URL>', required=False, dest='os_auth_url', help='(Optional) OpenStack authentication URL; can be omitted with setting env variable OS_AUTH_URL')

    parser_mount = subparser.add_parser('attach', help="Attach a storage volume to an instance for a user")
    parser_mount.add_argument('--user', required=False, dest='user', help='OpenStack user name')
    parser_mount.add_argument('--cinder-id', dest='cinder_id', help='volume ID of the Cinder volume to be attached')
    parser_mount.add_argument('--instance-id', dest='instance_id', help='instance ID to attach the volume to')
    parser_mount.add_argument('--dev-name', dest='dev_name', help='Device Name to attach the volume to')
    parser_mount.add_argument('--os-user', metavar='<OS_USERNAME>', required=False, dest='os_user', help='(Optional) Alias for the OpenStack user for connecting to the Cinder API service; can be omitted with setting env variable OS_USERNAME')
    parser_mount.add_argument('--os-password', metavar='<OS_PASSWORD>', required=False, dest='os_password', help='(Optional) Password for the OpenStack user; can be omitted with setting env variable OS_PASSWORD')
    parser_mount.add_argument('--os-tenant-name', metavar='<OS_TENANT_NAME>', required=False, dest='os_tenant_name', help='(Optional) OpenStack tenant (project) name; can be omitted with setting env variable OS_TENANT_NAME')
    parser_mount.add_argument('--os-auth-url', metavar='<OS_AUTH_URL>', required=False, dest='os_auth_url', help='(Optional) OpenStack authentication URL; can be omitted with setting env variable OS_AUTH_URL')

    return parser.parse_args()

def main():
    argv = parse_input()

    # Create a new task instance
    task = vmtask.Task()

    # Send credential info to task module
    if argv.task == 'mount':
        task.set_credentials(argv.host, argv.user, argv.key, argv.windows) # Check for error

    # Now call the specific task
    if argv.task == 'attach':
        ret = task.do_task(vmtask.TASKTYPE.TASK_SHARED_STORAGE, argv.user, argv.cinder_id, argv.instance_id, argv.dev_name, argv.os_user, argv.os_password, argv.os_tenant_name, argv.os_auth_url)
        if ret == -1:
            logging.critical("Some error")

    elif argv.task == 'mount':
        ret = task.do_task(vmtask.TASKTYPE.TASK_FORMAT_MOUNT, argv.format, argv.mountpoint, argv.cinder_id, argv.os_user, argv.os_password, argv.os_tenant_name, argv.os_auth_url)
        if ret == -1:
            logging.critical("Some error")


if __name__ == "__main__":
    main()
