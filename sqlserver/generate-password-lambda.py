import json
import random
import boto3
import logging
import traceback
from time import sleep
from botocore.vendored import requests
import json

SUCCESS = "SUCCESS"
FAILED = "FAILED"

def passwordgenerator():
    try:
        s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%^&*()?"
        passlen = 25
        p =  "".join(random.sample(s,passlen ))
        print ("Password Successfully Generated")
        return p
    
    except Exception as e:
        raise
    
    

def write2ssm(parameter_name, value, key):
    try:
        client = boto3.client('ssm')
    
        print ("Writing password to parameter specified.")
        response = client.put_parameter(
        Name= parameter_name,
        Value= value,
        Type='SecureString',
        KeyId= key,
        Overwrite=True,
        AllowedPattern="^[^\\/\"@]{8,}$"
        )
    except Exception as e:
        raise

def handler(event, context):
    try:
        parameterName = (event['ResourceProperties']['ParameterName'])
        keyId = (event['ResourceProperties']['KeyID'])
        # Generate password
        password = passwordgenerator()
        
        sleep(45) # Waiting 45 seconds to ensure IAM Permissions were properly propagated. 

        # Write password to SSM 
        write2ssm(parameterName, password, keyId)
        
        responseData = {}
        
        responseData['Data'] = "Success"
        send(event, context, SUCCESS, responseData, "CustomResourcePhysicalID")

    except Exception as e:
        logging.error(traceback.format_exc())
        responseData = {}
        responseData['Error'] = "Lambda Function was unable to successfully generate a password and place it in a SSM parameter"
        send(event, context, FAILED, responseData, "CustomResourcePhysicalID")
        raise

def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))