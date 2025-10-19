# My First AI Agent

A simple AI agent built with AWS Bedrock Agent Core and the Strands framework, powered by Claude 3.5 Sonnet. This agent can perform mathematical calculations and provide weather information.

## 🚀 Features

- **Mathematical Calculations**: Uses a calculator tool for solving math problems
- **Weather Information**: Provides weather updates (currently returns "sunny" as a demo)
- **AWS Bedrock Integration**: Deployed on AWS Bedrock Agent Core for scalable AI inference
- **Claude 3.5 Sonnet**: Powered by Anthropic's latest Claude model

## 📋 Prerequisites

- Python 3.9+
- AWS Account with Bedrock access
- AWS CLI configured with appropriate permissions
- Docker (for containerization)

## 🛠️ Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd my-first-agent
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv my-first-agent
   source my-first-agent/bin/activate  # On Windows: my-first-agent\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏗️ Project Structure

```
my-first-agent/
├── strands_claude.py          # Main agent implementation
├── create_agentruntime.py     # Runtime configuration and deployment
├── client.py                  # Client for testing the agent
├── requirements.txt           # Python dependencies
├── Dockerfile                # Container configuration
└── README.md                 # This file
```

## 🚀 Deployment

### Deploy to AWS Bedrock Agent Core

Run the deployment script to create and launch your agent:

```bash
python create_agentruntime.py
```

This script will:
- Configure the Bedrock Agent Core runtime
- Create necessary AWS resources (IAM roles, ECR repositories)
- Deploy your agent to AWS
- Provide you with an agent ARN for testing

## 🧪 Testing Your Agent

### Using the Client Script

Once deployed, you can test your agent using the provided client:

```bash
python client.py
```

The client will send a math problem ("What is the tan 60 + cos 60?") to your agent and display the response.

### Manual Testing

You can also invoke your agent directly using the AWS CLI or SDK with the agent ARN provided after deployment.

## 🔧 Customization

### Adding New Tools

To add new capabilities to your agent, create new tool functions in `strands_claude.py`:

```python
from strands import tool

@tool
def your_custom_tool():
    """Description of what your tool does"""
    # Your tool implementation
    return "tool result"

# Add to the agent's tools list
agent = Agent(
    model=model,
    tools=[calculator, weather, your_custom_tool],
    system_prompt="Your updated system prompt"
)
```

### Modifying the System Prompt

Update the `system_prompt` parameter in the Agent initialization to change how your agent behaves:

```python
agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a specialized math and weather assistant with a friendly personality."
)
```

## 📚 Key Components

### `strands_claude.py`
- Main agent implementation using the Strands framework
- Defines custom tools (calculator, weather)
- Sets up Claude 3.5 Sonnet model integration
- Contains the entrypoint function for AWS Bedrock

### `create_agentruntime.py`
- Handles AWS Bedrock Agent Core runtime configuration
- Automatically creates IAM roles and ECR repositories
- Deploys the agent to AWS infrastructure

### `client.py`
- Simple test client for invoking your deployed agent
- Demonstrates how to interact with the agent via AWS Bedrock

## 🔍 Troubleshooting

### Common Issues

1. **AWS Permissions**: Ensure your AWS credentials have the necessary permissions for Bedrock, IAM, and ECR services.

2. **Region Configuration**: Make sure you're deploying to a region where Bedrock is available (e.g., us-east-1).

3. **Model Access**: Verify that Claude 3.5 Sonnet is available in your AWS Bedrock console.

### Debug Mode

For debugging, you can run the agent locally by uncommenting the test code in `strands_claude.py`:

```python
if __name__ == "__main__":
    # Test locally
    response = strands_agent_bedrock({"prompt": "What is 2 + 2?"})
    print(response)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Strands Framework](https://github.com/strands-ai/strands) for the agent framework
- [AWS Bedrock Agent Core](https://aws.amazon.com/bedrock/) for the deployment platform
- [Anthropic Claude](https://www.anthropic.com/) for the AI model

---

**Note**: This is a learning project demonstrating how to build and deploy AI agents using AWS Bedrock and the Strands framework. For production use, consider adding proper error handling, logging, and security measures.