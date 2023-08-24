import boto3
import json

from botocore.exceptions import ClientError, NoCredentialsError


def get_secret(name: str, region: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region)
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidRequestException':
            print('The request was invalid due to:', e)
            exit()
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print('The request had invalid params:', e)
            exit()
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print('The requested secret can\'t be decrypted using the provided KMS key:', e)
            exit()
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print('An error occurred on service side:', e)
            exit()
        elif e.response['Error']['Code'] == 'ExpiredTokenException':
            print('An error occurred on service side:', e)
            exit()
        elif e.response['Error']['Code'] == 'AccessDeniedException':
            print(e)
            exit()
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            print('The requested secret ' + name + ' was not found')
            exit()
        else:
            raise e
    except NoCredentialsError as e:
        message = '''\nPlease set up AWS credential on your machine...

You can configure credentials by running "aws configure".
Alse you can use any other option like:

Option 1: Set AWS environment variables (Short-term credentials)
Option 2: Manually add a profile to your AWS credentials file (Short-term credentials)
Option 3: Use individual values in your AWS service client (Short-term credentials)'''
        print('An error occurred on client (your) side:', e)
        print(message)
        exit()
    else:
        return json.loads(get_secret_value_response['SecretString'])