# Lambda Bedrock API

API Gateway can expose a public HTTP route such as POST /summarize. The route integrates with Lambda. Lambda validates input, calls Bedrock Runtime, and returns JSON containing the summary, latency, token usage, and stop reason.

Frontend code should not directly call Bedrock because it would expose AWS credentials and make cost control, input validation, and logging harder.
