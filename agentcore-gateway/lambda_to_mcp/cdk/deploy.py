#!/usr/bin/env python3
"""
Deployment script that creates the Lambda function and prints all ARNs
"""

import subprocess
import json
import boto3
import sys

def deploy_stack():
    """Deploy the CDK stack"""
    print("Deploying CDK stack...")
    
    # Deploy the stack
    result = subprocess.run([
        "cdk", "deploy", "LambdaStack", "--require-approval", "never"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Deployment failed: {result.stderr}")
        return None
    
    print("Stack deployed successfully!")
    return True

def get_stack_outputs():
    """Get all stack outputs from CloudFormation"""
    print("Retrieving stack outputs...")
    
    try:
        # Initialize CloudFormation client with AWS profile
        session = boto3.Session(profile_name='myaws')
        cf_client = session.client('cloudformation')
        
        # Get stack outputs
        response = cf_client.describe_stacks(StackName='LambdaStack')
        
        if 'Stacks' in response and len(response['Stacks']) > 0:
            stack = response['Stacks'][0]
            outputs = stack.get('Outputs', [])
            
            lambda_arn = None
            lambda_name = None
            lambda_role_arn = None
            bedrock_role_arn = None
            user_pool_id = None
            user_pool_arn = None
            resource_server_id = None
            
            for output in outputs:
                if output['OutputKey'] == 'LambdaFunctionArn':
                    lambda_arn = output['OutputValue']
                    print(f"Lambda Function ARN: {lambda_arn}")
                elif output['OutputKey'] == 'LambdaFunctionName':
                    lambda_name = output['OutputValue']
                    print(f"Lambda Function Name: {lambda_name}")
                elif output['OutputKey'] == 'AgentCoreGatewayRoleArn':
                    lambda_role_arn = output['OutputValue']
                    print(f"AgentCore Gateway Role ARN: {lambda_role_arn}")
                elif output['OutputKey'] == 'AgentCoreBedrockRoleArn':
                    bedrock_role_arn = output['OutputValue']
                    print(f"AgentCore Bedrock Role ARN: {bedrock_role_arn}")
                elif output['OutputKey'] == 'CognitoUserPoolId':
                    user_pool_id = output['OutputValue']
                    print(f"Cognito User Pool ID: {user_pool_id}")
                elif output['OutputKey'] == 'CognitoUserPoolArn':
                    user_pool_arn = output['OutputValue']
                    print(f"Cognito User Pool ARN: {user_pool_arn}")
                elif output['OutputKey'] == 'CognitoResourceServerId':
                    resource_server_id = output['OutputValue']
                    print(f"Cognito Resource Server ID: {resource_server_id}")
            
            if lambda_arn and lambda_name and lambda_role_arn and bedrock_role_arn and user_pool_id and user_pool_arn and resource_server_id:
                return {
                    'lambda_arn': lambda_arn,
                    'lambda_name': lambda_name,
                    'lambda_role_arn': lambda_role_arn,
                    'bedrock_role_arn': bedrock_role_arn,
                    'user_pool_id': user_pool_id,
                    'user_pool_arn': user_pool_arn,
                    'resource_server_id': resource_server_id
                }
            else:
                print("Required outputs not found in stack")
                return None
        else:
            print("Stack not found")
            return None
            
    except Exception as e:
        print(f"Error retrieving outputs: {e}")
        return None

def main():
    """Main function"""
    print("=== CDK AgentCore Gateway Deployment Script ===")
    
    # Deploy the stack
    if deploy_stack():
        # Get and print all outputs
        outputs = get_stack_outputs()
        if outputs:
            print(f"\n✅ Success!")
            print(f"\n📋 Lambda Resources:")
            print(f"Lambda Function ARN: {outputs['lambda_arn']}")
            print(f"Lambda Function Name: {outputs['lambda_name']}")
            print(f"Lambda Execution Role ARN: {outputs['lambda_role_arn']}")
            print(f"\n🤖 AgentCore Resources:")
            print(f"AgentCore Bedrock Role ARN: {outputs['bedrock_role_arn']}")
            print(f"\n🔐 Cognito Resources:")
            print(f"User Pool ID: {outputs['user_pool_id']}")
            print(f"User Pool ARN: {outputs['user_pool_arn']}")
            print(f"Resource Server ID: {outputs['resource_server_id']}")
            print(f"\n📝 Next Steps:")
            print(f"1. Use the Lambda ARN to register with AgentCore Gateway")
            print(f"2. Use the Bedrock Role ARN for AgentCore integration")
            print(f"3. Use the Cognito User Pool ID for authentication")
            print(f"4. Use the Resource Server ID for OAuth scopes")
        else:
            print("\n❌ Failed to retrieve outputs")
            sys.exit(1)
    else:
        print("\n❌ Deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()