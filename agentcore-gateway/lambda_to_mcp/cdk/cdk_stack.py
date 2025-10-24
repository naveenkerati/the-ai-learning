#!/usr/bin/env python3
"""
CDK Stack for creating a Lambda function with ARN output
"""

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_cognito as cognito,
    CfnOutput,
    Duration,
    RemovalPolicy
)
from constructs import Construct


class LambdaStack(Stack):
    """CDK Stack that creates a Lambda function and outputs its ARN"""
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Create IAM role for AgentCore Gateway to call the lambda function
        agentcore_gateway_role = iam.Role(
            self, "AgentCoreBedrockRole",
            assumed_by=iam.ServicePrincipal("bedrock-agentcore.amazonaws.com"),
            managed_policies=[
                
            ],
            description="IAM role for AgentCore Gateway Lambda function"
        )
        agentcore_gateway_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock-agentcore:*",
                    "bedrock:*",
                    "agent-credential-provider:*",
                    "iam:PassRole",
                    "secretsmanager:GetSecretValue",
                    "lambda:InvokeFunction"
                ],
                resources=["*"]
            )
        )
    
       
      
        # Create IAM role for Lambda function with AgentCore Gateway permissions
        lambda_role = iam.Role(
            self, "AgentCoreGatewayRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ],
            description="IAM role for AgentCore Gateway Lambda function"
        )
        
        # Add additional permissions for AgentCore Gateway functionality
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream",
                    "bedrock:GetFoundationModel",
                    "bedrock:ListFoundationModels"
                ],
                resources=["*"]
            )
        )
        
        # Add permissions for CloudWatch Logs (for AgentCore logging)
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                resources=["*"]
            )
        )
        
        # Add permissions for S3 (if AgentCore needs to access S3)
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject"
                ],
                resources=["*"]
            )
        )
        
        # Create the Lambda function
        lambda_function = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function_code.lambda_handler",  # Updated handler to match the actual function name
            code=_lambda.Code.from_asset("lambda/lambda_function_code.zip"),  # CDK will automatically detect the zip file
            role=lambda_role,
            timeout=Duration.seconds(30),
            memory_size=128,
            description="A simple Lambda function created with CDK"
        )
        
        # Create Cognito User Pool
        user_pool = cognito.UserPool(
            self, "SampleAgentCoreGatewayPool",
            user_pool_name="sample-agentcore-gateway-pool"
        )
        
        #Create Cognito User Pool Domain
        
        # user_pool_domain = cognito.UserPoolDomain(
        #     self, "SampleAgentCoreGatewayDomain",
        #     user_pool=user_pool,
        #     cognito_domain=cognito.CognitoDomainOptions(
        #         domain_prefix=user_pool.user_pool_id.replace("_", "").lower()
        #     )
        # )
        
        # Create Cognito Resource Server
        resource_server = user_pool.add_resource_server(
            "SampleAgentCoreGatewayResourceServer",
            identifier="sample-agentcore-gateway-id",
            user_pool_resource_server_name="sample-agentcore-gateway-name",
            scopes=[
                cognito.ResourceServerScope(
                    scope_name="gateway:read",
                    scope_description="Read access"
                ),
                cognito.ResourceServerScope(
                    scope_name="gateway:write", 
                    scope_description="Write access"
                )
            ]
        )
        
        
        # Output the Lambda function ARN
        CfnOutput(
            self, "LambdaFunctionArn",
            value=lambda_function.function_arn,
            description="ARN of the Lambda function",
            export_name="LambdaFunctionArn"
        )
        
        # Also output the function name for reference
        CfnOutput(
            self, "LambdaFunctionName",
            value=lambda_function.function_name,
            description="Name of the Lambda function",
            export_name="LambdaFunctionName"
        )
        
        # Output the AgentCore Gateway role ARN
        CfnOutput(
            self, "AgentCoreGatewayRoleArn",
            value=lambda_role.role_arn,
            description="ARN of the AgentCore Gateway IAM role",
            export_name="AgentCoreGatewayRoleArn"
        )
        
        # Output Cognito User Pool information
        CfnOutput(
            self, "CognitoUserPoolId",
            value=user_pool.user_pool_id,
            description="ID of the Cognito User Pool",
            export_name="CognitoUserPoolId"
        )
        
        CfnOutput(
            self, "CognitoUserPoolArn",
            value=user_pool.user_pool_arn,
            description="ARN of the Cognito User Pool",
            export_name="CognitoUserPoolArn"
        )
        
        
        CfnOutput(
            self, "CognitoResourceServerId",
            value=resource_server.user_pool_resource_server_id,
            description="ID of the Cognito Resource Server",
            export_name="CognitoResourceServerId"
        )
        CfnOutput(
            self, "AgentCoreBedrockRoleArn",
            value=agentcore_gateway_role.role_arn,
            description="ARN of the AgentCore Bedrock Role",
            export_name="AgentCoreBedrockRoleArn"
        )
        
        # Output Cognito Domain information
        # CfnOutput(
        #     self, "CognitoUserPoolDomain",
        #     value=user_pool_domain.domain_name,
        #     description="Domain name of the Cognito User Pool",
        #     export_name="CognitoUserPoolDomain"
        # )
        
        # CfnOutput(
        #     self, "CognitoDomainUrl",
        #     value=f"https://{user_pool_domain.domain_name}.auth.{self.region}.amazoncognito.com",
        #     description="Full URL of the Cognito domain",
        #     export_name="CognitoDomainUrl"
        # )
