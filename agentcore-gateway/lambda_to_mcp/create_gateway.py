import boto3
gateway_client = boto3.client('bedrock-agentcore-control')
auth_config = {
    "customJWTAuthorizer":{
        "allowedClients":['2g18s8cva694tct9nbnq78ijq0','4jbq5ogmtq71mvk9d483ughlg1'],
        "discoveryUrl":"https://cognito-idp.us-east-1.amazonaws.com/us-east-1_NlwqZs1GE/.well-known/openid-configuration"
    }
}

create_response = gateway_client.create_gateway(name='TestGWforLambda',
    roleArn = 'arn:aws:iam::879381269713:role/LambdaStack-AgentCoreGatewayRoleB10592CC-CFQyKbI2bhQ3',
    protocolType='MCP',
    authorizerType='CUSTOM_JWT',
    authorizerConfiguration=auth_config, 
    description='AgentCore Gateway with AWS Lambda target type'
)

print(create_response)
# Retrieve the GatewayID used for GatewayTarget creation
gatewayID = create_response["gatewayId"]
gatewayURL = create_response["gatewayUrl"]
print(gatewayID)