import sys
import boto3
import os
import random

# List all instances
def list_instances(b):
	ec2 = boto3.resource('ec2')
	for instance in ec2.instances.all():
		print("\nInstance ID : ",instance.id, "\nState : ", instance.state,"\nLocation : ", instance.placement['AvailabilityZone'], "\nIP : ", instance.public_ip_address)
		if(instance.id==b):
			print("DNS:",instance.public_dns_name)
			print("Region",instance.placement['AvailabilityZone'])

# Create new instance
def create_instance(KeyPair, GroupId):
	ec2 = boto3.resource('ec2')
	instance = ec2.create_instances(ImageId='ami-f2d3638a', MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName = KeyPair, SecurityGroupIds = [GroupId])
	print("\nNew Instance Created \n Instance ID : ",instance[0].id)
	return instance[0].id

def create_key_pair(VarKeyName):
	ec2 = boto3.resource('ec2')
	outfile = open(VarKeyName+'.pem','w')
	key_pair = ec2.create_key_pair(KeyName=VarKeyName)
	KeyPairOut = str(key_pair.key_material)
	outfile.write(KeyPairOut)

def create_security_group(VarGroupName, VarGroupDescription):
	ec2 = boto3.resource('ec2')
	mysg = ec2.create_security_group(GroupName=VarGroupName, Description=VarGroupDescription)
	mysg.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)
	return mysg.id

def terminate_instance(b):
	ec2 = boto3.resource('ec2')
	#for instance_id in sys.argv[1:]:
	instance = ec2.Instance(b)
	response = instance.terminate()
	print("\nInstance Terminated:\n",response)
def silentremove(filename):
	if os.path.exists(filename+'.pem'):os.remove(filename+'.pem')
def deleteFromAWS(keyName):
	ec2 = boto3.client('ec2')
	response = ec2.delete_key_pair(KeyName=keyName)
# def deleteSecurityGroup(Name, GroupId):
# 	ec2 = boto3.client('ec2')
# 	ec2.delete_security_group(Name=secName,GroupId=SecGroupId,dry_run=True)
if __name__ == '__main__':
	keyName= "Key"
	randomValue = random.randint(1, 1000)
	secName = "Test"
	if (len(sys.argv) <2):
		silentremove(keyName)
		deleteFromAWS(keyName)
		create_key_pair(keyName)
		SecGroupId = create_security_group(secName+str(randomValue), "Security Group")
		InstanceId = create_instance(keyName, SecGroupId)
		# deleteSecurityGroup(secName, SecGroupId)
		list_instances(InstanceId)

		print("##################################################################################################")
		print("TO TERMINATE THE INSTANCE- RUN THE PROGRAM AGAIN AND GIVE THE INSTANCE-ID AS COMMAND LINE ARGUMENT")
		print("##################################################################################################")

	else:
		terminate_instance(sys.argv[1])
		print("Instance Was Terminated")
		silentremove(keyName)
		print("Delete Key Locally")
		deleteFromAWS(keyName)
		print("Deleted Key from AWS")
		# deleteSecurityGroup(secName, SecGroupId)
		# print("Delete Security Group")
