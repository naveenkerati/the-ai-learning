#!/usr/bin/env python3
"""
CDK App entry point
"""

from aws_cdk import App
from cdk_stack import LambdaStack

# Create the CDK app
app = App()

# Create the Lambda stack
lambda_stack = LambdaStack(
    app, "LambdaStack",
    description="Stack containing a Lambda function with ARN output"
)

# Synthesize the app
app.synth()
