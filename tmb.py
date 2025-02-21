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
import time
import threading
from queue import Queue

class TrustMeBro:
    """A multithreaded framework for testing AI model responses via REST API (Chat Completion)."""
    def __init__(self, api_url, model, auth_token=None, num_threads=1):
        self.api_url = f"{api_url}/v1/chat/completions"
        self.model = model
        self.auth_token = auth_token
        self.num_threads = num_threads
        self.queue = Queue()
        self.results = []
        self.lock = threading.Lock()

    def get_response(self, prompt):
        """Send a prompt to the AI model using chat completion and return the response."""
        headers = {"Authorization": f"Bearer {self.auth_token}", "Content-Type": "application/json"} if self.auth_token else {"Content-Type": "application/json"}
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        start_time = time.time()
        response = requests.post(self.api_url, json=data, headers=headers)
        response.raise_for_status()
        end_time = time.time()
        response_time = end_time - start_time
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response received").strip(), response_time

    def worker(self):
        """Thread worker function to process the test cases."""
        while not self.queue.empty():
            test_file, test_case = self.queue.get()
            prompt = test_case.get("prompt")
            expected = test_case.get("expected")
            
            print(f"Running test: {test_file}")
            response, response_time = self.get_response(prompt)
            success = expected in response
            
            with self.lock:
                self.results.append({"test": test_file, "success": success, "expected": expected, "actual": response, "response_time": response_time})
            
            print(f"✅ {test_file} ({response_time:.2f}s)" if success else f"❌ {test_file} (Expected: {expected}, Got: {response}, Time: {response_time:.2f}s)")
            self.queue.task_done()

    def run_tests(self, test_dir):
        """Load and execute test cases from a directory in multiple threads."""
        for test_file in os.listdir(test_dir):
            if test_file.endswith(".json"):
                with open(os.path.join(test_dir, test_file), "r") as f:
                    test_case = json.load(f)
                    self.queue.put((test_file, test_case))
        
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        print("\nTest Summary:")
        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)
        avg_response_time = sum(r["response_time"] for r in self.results) / total if total > 0 else 0
        print(f"{passed}/{total} tests passed")
        print(f"Average response time: {avg_response_time:.2f} seconds")
        return self.results


def main():
    parser = argparse.ArgumentParser(prog="TMB", description="TrustMeBro: AI Model Testing Framework")
    parser.add_argument("api_url", type=str, help="REST API URL of the AI model")
    parser.add_argument("test_dir", type=str, help="Directory containing test cases in JSON format")
    parser.add_argument("--model", type=str, required=True, help="Model identifier")
    parser.add_argument("--auth_token", type=str, default=None, help="Optional authentication token")
    parser.add_argument("--threads", type=int, default=1, help="Number of threads to use (default: 1)")
    args = parser.parse_args()
    
    framework = TrustMeBro(args.api_url, args.model, args.auth_token, args.threads)
    framework.run_tests(args.test_dir)

if __name__ == "__main__":
    main()