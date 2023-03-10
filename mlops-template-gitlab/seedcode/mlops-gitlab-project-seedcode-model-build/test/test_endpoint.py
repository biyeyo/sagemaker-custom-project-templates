#!/usr/bin/env python

import os
import sys
import json
import yaml
import boto3
import random

sagemaker = boto3.client("sagemaker-runtime")

def test_endpoint(endpoint_name, payload):
    try:
        response = sagemaker.invoke_endpoint(EndpointName=endpoint_name,
                                             ContentType="application/json",
                                             Accept="application/json",
                                             Body=payload)
        return {
            "statusCode": 200,
            "body": json.loads(response["Body"].read().decode("utf-8"))
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": repr(e)}),
        }

if __name__ == "__main__":
    # READ CONFIG FILE
    with open("cfg/model_deploy.yaml") as f: config = yaml.load(f, Loader=yaml.SafeLoader)
    
    # READ PAYLOADS SAMPLE
    payload_list = [os.path.join('src/data', f) for f in os.listdir('src/data') if f.endswith('.json')]
    
    # GET ENDPOINT NAME FROM CONFIG AND DEPLOYMENT ENVIRONMENT
    endpoint_name = "{}-{}".format(config['endpoint']['name'], os.getenv('DEPLOYMENT_ENV'))
    
    # SEND A TEST DATA POINT TO THE API AND VERIFYING THE RESPONSE STATUS CODE
    # TEST FOR 100 HUNDRED PAYLOAD INJECTIONS TO THE ENDPOINT 
    for _ in range(100):
        test_payload = json.load(open(random.sample(payload_list,1)[0]))
        print("TESTING INPUT DATA TO THE ENDPOINT:\n{}".format(test_payload))
        results = test_endpoint(endpoint_name, json.dumps(test_payload))
        if results["statusCode"]==500:
            sys.exit("Invocation error" )
        print("TESTING RESPONSE FROM THE ENDPOINT:\n{}".format(json.dumps(results, indent=4, default=str)))
