import boto3 # pip install boto3

# Set the region and the name of the autoscaling group
region = 'us-west-2'
autoscaling_group_name = 'my-autoscaling-group'

# Create an EC2 client and an Autoscaling client
ec2_client = boto3.client('ec2', region_name=region)
autoscaling_client = boto3.client('autoscaling', region_name=region)

# Get the list of instances in the autoscaling group
instances = []
response = autoscaling_client.describe_auto_scaling_groups(
    AutoScalingGroupNames=[autoscaling_group_name]
)
for group in response['AutoScalingGroups']:
    for instance in group['Instances']:
        instances.append(instance['InstanceId'])

# Get the public IPs of the live instances in the autoscaling group
ips = []
response = ec2_client.describe_instances(InstanceIds=instances)
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if instance['State']['Name'] == 'running':
            ips.append(instance['PublicIpAddress'])

# Print the list of live IPs
print(ips)
