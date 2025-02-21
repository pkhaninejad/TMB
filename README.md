# TrustMeBro (TMB) - AI Model Testing Framework

TrustMeBro (TMB) is a lightweight CLI tool for testing AI model responses using REST API endpoints. It loads test cases from a directory, sends prompts to the AI model, and verifies the responses against expected results.

## Features
- Supports OpenAI-style chat completion API
- Loads test cases from JSON files in a directory
- Executes tests using the Arrange, Act, and Assert pattern
- Supports authentication via bearer token
- Includes a configurable request timeout
- Supports multi-threading for faster test execution
- Summarizes test results with pass/fail counts and response times

## Installation
Ensure you have Python 3.12 or later with [uv](https://github.com/astral-sh/uv) installed.


## Usage
### Running Tests
```sh
uv run tmb.py <API_URL> <TEST_DIR> --model <MODEL_NAME> [--auth_token <TOKEN>] [--timeout <SECONDS>] [--threads <NUM_THREADS>]
```

### Example
```sh
uv run tmb.py https://api.example.com examples --model deepseek-r1-distill-qwen-32b --auth_token my-secret-token --threads 4
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

## Local LLM Testing
For testing, we used local LLMs running on our machines using [Ollama](https://ollama.com/) and [LM Studio](https://lmstudio.ai/). These tools allow for efficient and private model execution without relying on external APIs.

## Test Results
Reading inline script metadata from `tmb.py`

```
Running test: sentence_completion.json
Running test: fact_check.json
✅ fact_check.json (62.50s)
Running test: trivia_question.json
✅ sentence_completion.json (105.03s)
Running test: definition_test.json
✅ trivia_question.json (99.11s)
Running test: programming_output.json
❌ definition_test.json (Expected: lasting for a very short time, Got: <think> ...
Running test: simple_logic.json
✅ programming_output.json (160.98s)
Running test: antonym.json
✅ simple_logic.json (154.71s)
Running test: historical_data_question.json
✅ antonym.json (177.88s)
Running test: common_knowlege.json
✅ historical_data_question.json (108.62s)
Running test: boolean_logic.json
✅ common_knowlege.json (63.59s)
Running test: riddle_test.json
✅ boolean_logic.json (119.66s)
Running test: basic_math.json
✅ riddle_test.json (125.66s)
Running test: basic_science.json
✅ basic_math.json (71.12s)
Running test: synonym_test.json
✅ basic_science.json (74.21s)
Running test: currency_conversion.json
✅ synonym_test.json (129.51s)
✅ currency_conversion.json (194.92s)

Test Summary:
14/15 tests passed
Average response time: 118.87 seconds
```

## License
MIT License

## Contributions
Feel free to submit issues and pull requests to improve the framework!

