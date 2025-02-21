# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///
import requests
import argparse
import os
import json

class TrustMeBro:
    """A simple framework for testing AI model responses via REST API (Chat Completion)."""
    def __init__(self, api_url, auth_token=None):
        self.api_url = f"{api_url}/v1/chat/completions"
        self.auth_token = auth_token

    def get_response(self, prompt):
        """Send a prompt to the AI model using chat completion and return the response."""
        headers = {"Authorization": f"Bearer {self.auth_token}", "Content-Type": "application/json"} if self.auth_token else {"Content-Type": "application/json"}
        data = {
            "model": "deepseek-r1-distill-qwen-32b",  # Default model, can be adjusted per API
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(self.api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response received").strip()

    def run_tests(self, test_dir):
        """Load and execute test cases from a directory."""
        results = []
        for test_file in os.listdir(test_dir):
            if test_file.endswith(".json"):
                with open(os.path.join(test_dir, test_file), "r") as f:
                    test_case = json.load(f)
                    prompt = test_case.get("prompt")
                    expected = test_case.get("expected")
                    
                    print(f"Running test: {test_file}")
                    response = self.get_response(prompt)
                    success = expected in response
                    results.append({"test": test_file, "success": success, "expected": expected, "actual": response})
                    print(f"✅ {test_file}" if success else f"❌ {test_file} (Expected: {expected}, Got: {response})")
        
        print("\nTest Summary:")
        passed = sum(1 for r in results if r["success"])
        total = len(results)
        print(f"{passed}/{total} tests passed")
        return results


def main():
    parser = argparse.ArgumentParser(prog="TMB", description="TrustMeBro: AI Model Testing Framework")
    parser.add_argument("api_url", type=str, help="REST API URL of the AI model")
    parser.add_argument("test_dir", type=str, help="Directory containing test cases in JSON format")
    parser.add_argument("--auth_token", type=str, default=None, help="Optional authentication token")
    args = parser.parse_args()
    
    framework = TrustMeBro(args.api_url, args.auth_token)
    framework.run_tests(args.test_dir)

if __name__ == "__main__":
    main()
