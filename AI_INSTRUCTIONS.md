# Cursor Rules for API Auto-Test MCP

To ensure the AI Agent effectively uses the API Auto-Test MCP tools, you can add the following rules to your project's `.cursor/rules` (or `.cursorrules`) file.

## 1. Define Tool Triggers
Explicitly tell the AI when to reach for the tool instead of writing code or hallucinating functionality.

```markdown
# API Testing & Simulation Rules

When the user asks to "test an API", "check an endpoint", or "verify a curl command":
1.  **Do NOT** assume success or mock responses.
2.  **Use the `api-tester` MCP server** tools.
3.  For curl commands, use `run_curl(command=...)`.
4.  For simulating mobile devices (iOS/Android), use `simulate_client_request`.
5.  Always generate a test report using `export_test_report` after a batch of tests.
```

## 2. Example Usage Prompts
You can copy-paste these prompts to get the AI to do exactly what you want.

### Scenario A: Testing a specific endpoint as an iPhone
> "Test the endpoint POST http://localhost:8088/api/v1/login as an iPhone user. The payload is { 'email': 'admin@test.com', 'password': '123' }. Check if it responds under 500ms."

### Scenario B: Running a complex CURL from a file
> "I have a complex curl command in `login.txt`. Please read usage of `run_curl` tool and then execute that command using the tool to verify it works."

### Scenario C: Full Regression Suite
> "Run a sequence of tests:
> 1. Login as Android (simulate_client_request).
> 2. Use the token to GET /profile.
> 3. Export the results to a markdown report named 'daily_regression_run'."

## 3. Best Practices for Tool Descriptions (Developer Side)
If you are modifying the python code, keep these docstrings clear:

*   **Bad:** `def run(cmd):` -> AI doesn't know what `cmd` is.
*   **Good:** `def run_curl(command: str): "Executes a raw curl command string..."` -> AI understands it handles strings directly.

## 4. Troubleshooting
If the AI says "I don't have that tool":
*   Check `Cursor Settings > Features > MCP` to ensure `api-tester` is green (Connected).
*   Restart Cursor to refresh the tool definition cache.
