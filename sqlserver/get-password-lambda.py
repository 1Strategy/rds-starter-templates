import json
import boto3
import logging
import traceback
from botocore.vendored import requests

SUCCESS = "SUCCESS"
FAILED = "FAILED"

def getssmparameter(parameter_name):
    try:
        client = boto3.client('ssm')
        
        print ("Getting password from parameter specified.")
        response = client.get_parameter(
        Name= parameter_name,
        WithDecryption=True
        )
        
        return response
    
    except Exception as e:
        raise

def handler(event, context):
    try:
        parameterName = (event['ResourceProperties']['ParameterName'])
        
        # Get password from SSM 
        response = getssmparameter(parameterName)
        
    
        responseData = {}
        
        responseData['Data'] = response['Parameter']['Value']
        send(event, context, SUCCESS, responseData, "CustomResourcePhysicalID",noEcho=True) #Need to remove sensitive data from logs

    except Exception as e:
        logging.error(traceback.format_exc())
        responseData = {}
        responseData['Error'] = "Lambda Function was unable to successfully retrieve the password from the SSM parameter"
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

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code - " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..) -" + str(e))
