import boto3
import json
agent_arn = 'arn:aws:bedrock-agentcore:us-east-1:879381269713:runtime/strands_claude_getting_started-Z3Xad495Ui'

agentcore_client = boto3.client('bedrock-agentcore', region_name='us-east-1')
response = agentcore_client.invoke_agent_runtime(
    agentRuntimeArn=agent_arn,
    qualifier="DEFAULT",
    payload=json.dumps({"prompt": "What is the tan 60 + cos 60?"})
)
response_body = response['response'].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
# if "text/event-stream" in boto3_response.get("contentType", ""):
#     content = []
#     for line in boto3_response["response"].iter_lines(chunk_size=1):
#         if line:
#             line = line.decode("utf-8")
#             if line.startswith("data: "):
#                 line = line[6:]
#                 print(line)
#                 content.append(line)
#     display(Markdown("\n".join(content)))
# else:
#     try:
#         events = []
#         for event in boto3_response.get("response", []):
#             events.append(event)
#     except Exception as e:
#         events = [f"Error reading EventStream: {e}"]
#     display(Markdown(json.loads(events[0].decode("utf-8"))))
