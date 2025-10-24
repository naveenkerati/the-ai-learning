import boto3
gateway_client = boto3.client('bedrock-agentcore-control')
lambda_target_config = {
    "mcp": {
        "lambda": {
            "lambdaArn": 'arn:aws:lambda:us-east-1:879381269713:function:LambdaStack-MyLambdaFunction67CCA873-cTHvTTKlIB9x', # Replace this with your AWS Lambda function ARN
            "toolSchema": {
                "inlinePayload": [
                    {
                        "name": "get_order_tool",
                        "description": "tool to get the order",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "orderId": {
                                    "type": "string"
                                }
                            },
                            "required": ["orderId"]
                        }
                    },                    
                    {
                        "name": "update_order_tool",
                        "description": "tool to update the orderId",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "orderId": {
                                    "type": "string"
                                }
                            },
                            "required": ["orderId"]
                        }
                    }
                ]
            }
        }
    }
}

credential_config = [ 
    {
        "credentialProviderType" : "GATEWAY_IAM_ROLE"
    }
]
targetname='LambdaUsingSDK'
response = gateway_client.create_gateway_target(
    gatewayIdentifier='testgwforlambda-dw2ajtoutm',
    name=targetname,
    description='Lambda Target using SDK',
    targetConfiguration=lambda_target_config,
    credentialProviderConfigurations=credential_config)