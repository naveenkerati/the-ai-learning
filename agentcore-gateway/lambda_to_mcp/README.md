# AgentCore Gateway Lambda Function with Cognito Authentication

This project contains a CDK script that creates an AgentCore Gateway Lambda function with Cognito User Pool authentication and resource server configuration.

## Architecture

- **Lambda Function**: AgentCore Gateway function with Bedrock permissions
- **Cognito User Pool**: Authentication and authorization
- **Cognito Resource Server**: OAuth scopes for API access
- **IAM Roles**: AgentCore Bedrock role and Lambda execution role

## Files

- `cdk/cdk_stack.py` - Main CDK stack definition
- `cdk/app.py` - CDK app entry point
- `cdk/deploy.py` - Deployment script that prints all ARNs
- `cdk/cdk.json` - CDK configuration
- `lambda/lambda_function_code.zip` - Lambda function code
- `get_token.py` - Cognito token retrieval utility
- `register_lambda_gateway.py` - AgentCore Gateway registration

## Setup

1. Install dependencies:
```bash
cd cdk
pip install -r requirements.txt
```

2. Bootstrap CDK (if not already done):
```bash
cdk bootstrap
```

3. Configure AWS profile (optional):
```bash
export AWS_PROFILE=myaws
```

## Deployment

### Option 1: Using the deployment script
```bash
cd cdk
python deploy.py
```

### Option 2: Manual deployment
```bash
cd cdk
# Deploy the stack
cdk deploy LambdaStack

# The ARNs will be printed in the outputs section
```

### Option 3: Using CDK directly
```bash
cd cdk
# Synthesize the CloudFormation template
cdk synth

# Deploy the stack
cdk deploy --require-approval never
```

## Outputs

After deployment, the stack will output:
- `LambdaFunctionArn` - The ARN of the created Lambda function
- `LambdaFunctionName` - The name of the Lambda function
- `AgentCoreGatewayRoleArn` - The ARN of the Lambda execution role
- `AgentCoreBedrockRoleArn` - The ARN of the AgentCore Bedrock role
- `CognitoUserPoolId` - The ID of the Cognito User Pool
- `CognitoUserPoolArn` - The ARN of the Cognito User Pool
- `CognitoResourceServerId` - The ID of the Cognito Resource Server

## Cleanup

To remove the stack:
```bash
cd cdk
cdk destroy LambdaStack
```

## Lambda Function Details

The created Lambda function:
- **Runtime**: Python 3.11
- **Handler**: `lambda_function_code.lambda_handler`
- **Memory**: 128 MB
- **Timeout**: 30 seconds
- **Code Source**: Uses the zip file in `lambda/lambda_function_code.zip`
- **Permissions**: Bedrock, CloudWatch Logs, S3 access
- **Purpose**: AgentCore Gateway function for tool execution

## Cognito Configuration

### User Pool
- **Name**: `sample-agentcore-gateway-pool`
- **Self-signup**: Enabled
- **Password Policy**: 8+ characters with complexity requirements

### Resource Server
- **ID**: `sample-agentcore-gateway-id`
- **Name**: `sample-agentcore-gateway-name`
- **Scopes**:
  - `gateway:read` - Read access
  - `gateway:write` - Write access

## IAM Roles

### Lambda Execution Role
- **Name**: `AgentCoreGatewayRole`
- **Permissions**: Bedrock, CloudWatch Logs, S3
- **Purpose**: Lambda function execution

### AgentCore Bedrock Role
- **Name**: `AgentCoreBedrockRole`
- **Permissions**: Bedrock, AgentCore, IAM PassRole, Secrets Manager
- **Purpose**: AgentCore Gateway integration

## Usage

1. **Deploy the stack** using one of the deployment methods above
2. **Get the outputs** from the deployment script
3. **Register with AgentCore** using the Lambda ARN and Bedrock role ARN
4. **Configure authentication** using the Cognito User Pool ID and Resource Server ID

## Authentication Flow

1. **Client Credentials**: Use Cognito for machine-to-machine authentication
2. **OAuth Scopes**: Request `gateway:read` and `gateway:write` scopes
3. **API Access**: Use tokens to access protected endpoints
4. **Tool Execution**: Lambda function processes AgentCore tool requests
