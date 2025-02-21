# TrustMeBro (TMB) - AI Model Testing Framework

TrustMeBro (TMB) is a lightweight CLI tool for testing AI model responses using REST API endpoints. It loads test cases from a directory, sends prompts to the AI model, and verifies the responses against expected results.

## Features
- Supports OpenAI-style chat completion API
- Loads test cases from JSON files in a directory
- Executes tests using the Arrange, Act, and Assert pattern
- Supports authentication via bearer token
- Includes a configurable request timeout
- Summarizes test results with pass/fail counts
- Measures response time for each test case and calculates the average response time
- Allows specifying the AI model identifier via CLI

## Installation
Ensure you have Python 3.12 or with [uv](https://github.com/astral-sh/uv) installed. Install dependencies:

## Usage
### Running Tests
```sh
uv run tmb.py <API_URL> <TEST_DIR> [--auth_token <TOKEN>] [--timeout <SECONDS>] [--model <MODEL_ID>]
```

### Example
```sh
uv run tmb.py https://api.example.com tests --auth_token my-secret-token --model deepseek-r1-distill-qwen-32b
```

## Test Case Format
Each test case should be a JSON file inside the test directory with the following structure:
```json
{
    "prompt": "What is 1 + 1?",
    "expected": "2"
}
```

## API Configuration
TMB automatically appends `/v1/chat/completions` to the provided API URL. Ensure your API follows the OpenAI-style request format.

## License
MIT License

## Contributions
Feel free to submit issues and pull requests to improve the framework!
