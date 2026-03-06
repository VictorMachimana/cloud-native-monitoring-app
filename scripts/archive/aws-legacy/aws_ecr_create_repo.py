import boto3

ecr_client = boto3.client('ecr')

repo_name='cloud-system-monitoring-app'

response = ecr_client.create_repository(repositoryName=repo_name)

responseUri = response['repository']['repositoryUri']

# print({responseUri})