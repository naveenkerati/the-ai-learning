from strands.models import BedrockModel
from mcp.client.streamable_http import streamablehttp_client 
from strands.tools.mcp.mcp_client import MCPClient
from strands import Agent
import boto3
import logging
import json
import requests



print("Requesting the access token from Amazon Cognito authorizer...")
user_pool_id = 'us-east-1_f0E678Sng' #replace with the user pool id of the app client
client_id = '4jbq5ogmtq71mvk9d483ughlg1' #replace with the client id of the app client
client_secret = 'n1l8re15pu95k5odgf7glg7l445c66dsedpc2qkrrgmfpc01esr' #replace with the client secret of the app client
scopeString = 'sample-agentcore-gateway-id/gateway:read sample-agentcore-gateway-id/gateway:write'
REGION = 'us-east-1'
RESOURCE_SERVER_ID = 'sample-agentcore-gateway-id'

def get_token(user_pool_id: str, client_id: str, client_secret: str, scope_string: str, REGION: str) -> dict:
    try:
        user_pool_id_without_underscore = user_pool_id.replace("_", "")
        url = f"https://{user_pool_id_without_underscore}.auth.{REGION}.amazoncognito.com/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope_string,

        }
        print(client_id)
        response = requests.post(url, headers=headers, data=data)
        print(response.json())
        return response.json()

    except requests.exceptions.RequestException as err:
        return {"error": str(err)}
token_response = get_token(user_pool_id, client_id, client_secret,scopeString,REGION)
token = token_response['access_token']
print("Token response:", token)
