import subprocess

import sys

import argparse



def listChoice(question, func, args):
	print question
	spot = 0
	for spot, item in enumerate(args):
		print "%d) %s" % (spot, item)
	print "%d) EXIT" % (spot+1)
	try:
		testInput = int(raw_input(">>"), 10)
	except ValueError:
		print "Please enter a number and not a string."
		func(args)
		return
	else:
		if testInput > len(args)+1:
			print "The number must be less than %d.  Please try again." % len(vmNames)
			func(args)
		elif testInput == len(args):
			sys.exit(0)
		return args[testInput]

def getNameVM():
	nameList = []
	sp = subprocess.Popen(['VBoxManage', 'list', 'vms'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = sp.communicate()
	line = stdout.split('\n')
	for item in line:
		if len(item) > 0:
			print item
			print item.rsplit('{')
			nameList.append(item.rsplit('{')[0].rstrip())
	if not len(nameList) > 0:
		print "There are no VMs on this system."
		print "Please Press Enter to Exit."
		raw_input()
		sys.exit(0)
	return nameList

def listChoicesNameVM(vmNames):
	return listChoice("Which VM?", listChoicesNameVM, vmNames)

def getSnapshot(vmName):
	vmName = vmName.replace('"', '')
	sp = subprocess.Popen(['VBoxManage', 'snapshot', vmName, 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = sp.communicate()
	if sp.returncode == 0:
		snapFullName = output.split('\n')
		snapFullName = [string.lstrip().rstrip() for string in snapFullName]
		snapFullName = filter(None, snapFullName)
		snapUUID = [string.split('(', 1)[1].split(')')[0] for string in snapFullName]
		snapNames = [string.split('Name: ', 1)[1].split('(', 1)[0].lstrip().rstrip() for string in snapFullName]
		snapDict = dict(zip(snapNames, snapUUID))
		return snapNames, snapDict
	else:
		print "There are no snapshots for this Virtual Box."
		
def listChoiceSnap(snapNames):
	return listChoice("Please choose a snapshot to restore from.", listChoiceSnap, snapNames)

def restoreSnapshot(snapName, vmName):
	vmName = vmName.replace('"', '')
	snapName = snapName.replace('"', '')
	sp = subprocess.Popen(['vboxmanage', 'snapshot', vmName, 'restore', snapName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = sp.communicate()
	print output

def giveChoices(*args):
	choices = ["StartVM", "Restore Snapshot"]
	return listChoice("Please choose an option.", giveChoices, choices)

def startVM(vmName):
	vmName = vmName.replace('"', '')
	sp = subprocess.Popen(['vboxmanage', 'startvm', vmName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = sp.communicate()
	print output
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-startvm", action="store_true")
	args = parser.parse_args()
	if args.startvm:
		print 'yes'
	initialChoice = giveChoices()
	namesVM = getNameVM()
	vmName = listChoicesNameVM(namesVM)
	if initialChoice == "StartVM":
		snapNames, snapDict = getSnapshot(vmName)
		snapName = listChoiceSnap(snapNames)
		restoreSnapshot(snapName, vmName)
		startVM(vmName)
	else:
		snapNames, snapDict = getSnapshot(vmName)
		snapName = listChoiceSnap(snapNames)
		restoreSnapshot(snapName, vmName)

if __name__ == '__main__':
	main()
