#!/usr/bin/python
# coding: utf-8
from subprocess import PIPE
import subprocess
import re
import string

def get_blocks():

	cmd = subprocess.Popen("sudo lsblk --output NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT",shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]
	cmd =  cmd.replace('├─','')		# Special characters have been removed
	cmd =  cmd.replace('└─','')
	data = re.split('[\n]',cmd)		# Reading the command output line by line
	for i in range(len(data)):
		data[i]=re.sub("\s\s+" , " ", data[i])	# Replacing multiple spaces in the line with a single space
		
	info_new = []		# List to store the device names ,type (disk/part) and volume size of those devices which are neither formatted 
						# nor mounted. Index [0,3,6....] stores the device name & index [1,4,7....] store the device size & index [2.5.8..]
						# store the device type
	info_fs = []		# List to store the device name,volume size,type and file system of those devices which are formatted but not 
						# mounted. Index [0,4,8...] stores the device name index [1,5,9,...] store the device size, index [2,6,10,..] store 
						# the type and index [3,7,11,.....] store the file system

	for i in range(len(data)):
		if i>0:			# This has been done assuming that the first entry would be the heading of the columns
			finaldata = re.split(' ',data[i])	# Each line is split on the basis of spaces
			
			if len(finaldata)==4:
				info_new.append(finaldata[0])
				info_new.append(finaldata[1])
				info_new.append(finaldata[2])


			elif (len(finaldata)==5 and finaldata[4]==""):
				info_fs.append(finaldata[0])
				info_fs.append(finaldata[1])
				info_fs.append(finaldata[2])
				info_fs.append(finaldata[3])
			
	for i in range(len(info_new)):
		print "[%s]=%s" %(i,info_new[i])
	print "\n\n"

	print "info_fs"
	for i in range(len(info_fs)):
		print "[%s]=%s" %(i,info_fs[i])
	print "\n\n"

