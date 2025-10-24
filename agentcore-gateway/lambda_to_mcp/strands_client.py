from strands.models import BedrockModel
from mcp.client.streamable_http import streamablehttp_client 
from strands.tools.mcp.mcp_client import MCPClient
from strands import Agent
import logging
token = "eyJraWQiOiJwYXg3Q0w0SWUzSjRQZm9MNXJCeGZZVnhKMFVJS1J4dTBoOEtJNmtBWXRzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI0amJxNW9nbXRxNzFtdms5ZDQ4M3VnaGxnMSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoic2FtcGxlLWFnZW50Y29yZS1nYXRld2F5LWlkXC9nYXRld2F5OndyaXRlIHNhbXBsZS1hZ2VudGNvcmUtZ2F0ZXdheS1pZFwvZ2F0ZXdheTpyZWFkIiwiYXV0aF90aW1lIjoxNzYxMjU5NzU2LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9mMEU2NzhTbmciLCJleHAiOjE3NjEyNjMzNTYsImlhdCI6MTc2MTI1OTc1NiwidmVyc2lvbiI6MiwianRpIjoiYjQ3ZjA2ZDUtNzNjYi00YjhhLTkzNGEtMGYxMTM0NTAyMTA1IiwiY2xpZW50X2lkIjoiNGpicTVvZ210cTcxbXZrOWQ0ODN1Z2hsZzEifQ.idGiIDDlhKltSq-PM8wVnS0C7EpftIyJRsKstwBWUQw8_sGgLRWwhaGVHITX-IQOSnVlHTz1NDs3LlMaNZeaGzp0_7cb8zcSIWnJr04WVzrzW58ryuBI-PRjJtq1Il90YDe0kovYuT26SUG9GqfPcH687j0RM2NRqBS-Jkz3cwQka8zbtiCX9u0CKhpXqtFNqZCvcjoC9JsEL8yV5AI1-Sa2--wwT8pQ_LnXfkoGbjb_b6Ueq9qwnYD3Zu-bgVI25Ywix8NVbR4If22QB5vf7HHqVvgI_z6oQvU5n1NO6a_JkixGIhb0jGQJurEHRrRhh39WxcoLH4Hpe2G4VX-HXA"
gatewayURL = 'https://testgwforlambda-dw2ajtoutm.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp'
def create_streamable_http_transport():
    return streamablehttp_client(gatewayURL,headers={"Authorization": f"Bearer {token}"})

client = MCPClient(create_streamable_http_transport)

## The IAM credentials configured in ~/.aws/credentials should have access to Bedrock model
yourmodel = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",
    temperature=0.7,
)
# Configure the root strands logger. Change it to DEBUG if you are debugging the issue.
logging.getLogger("strands").setLevel(logging.INFO)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", 
    handlers=[logging.StreamHandler()]
)
targetname='LambdaUsingSDK'
with client:
    # Call the listTools 
    tools = client.list_tools_sync()
    # Create an Agent with the model and tools
    agent = Agent(model=yourmodel,tools=tools) ## you can replace with any model you like
    print(f"Tools loaded in the agent are {agent.tool_names}")
    # print(f"Tools configuration in the agent are {agent.tool_config}")
    # Invoke the agent with the sample prompt. This will only invoke  MCP listTools and retrieve the list of tools the LLM has access to. The below does not actually call any tool.
    agent("Hi , can you list all tools available to you")
    # Invoke the agent with sample prompt, invoke the tool and display the response
    agent("Check the order status for order id 123 and show me the exact response from the tool")
    # Call the MCP tool explicitly. The MCP Tool name and arguments must match with your AWS Lambda function or the OpenAPI/Smithy API
    result = client.call_tool_sync(
    tool_use_id="get-order-id-123-call-1", # You can replace this with unique identifier. 
    name=targetname+"___get_order_tool", # This is the tool name based on AWS Lambda target types. This will change based on the target name
    arguments={"orderId": "123"}
    )
    # Print the MCP Tool response
    print(f"Tool Call result: {result['content'][0]['text']}")