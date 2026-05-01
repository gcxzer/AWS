# Project 3: Python Serverless API

This project starts with a Lambda handler that mimics an API Gateway HTTP API event and persists notes in DynamoDB.

Status:

```text
Local code is kept for learning and rebuild.
AWS resources were deleted on 2026-05-01.
```

Architecture:

```text
Client / curl
  -> API Gateway HTTP API
  -> Lambda function
  -> DynamoDB table
  -> CloudWatch Logs
```

Service roles:

```text
API Gateway = public HTTPS entry point and routing
Lambda = Python business logic
DynamoDB = persistent notes storage
IAM execution role = permissions Lambda uses at runtime
CloudWatch Logs = Lambda runtime logs
CloudTrail = AWS account management audit log
```

Current behavior:

- `GET /notes` scans the DynamoDB table and returns notes.
- `POST /notes` creates a note in DynamoDB from JSON request body.
- `GET /notes/{id}` reads one note from DynamoDB.
- `DELETE /notes/{id}` deletes one note from DynamoDB.
- Unsupported routes return `404`.

Required DynamoDB table:

```text
Table name: learning-notes
Partition key: id (String)
Billing mode: On-demand
```

Deleted AWS resources:

```text
Region: eu-central-1
Lambda function: learning-notes-api (deleted)
Lambda execution role: learning-notes-lambda-role (deleted)
Auto-created Lambda role: learning-notes-api-role-nu8fie6u (deleted)
DynamoDB table: learning-notes (deleted)
HTTP API: learning-notes-http-api (deleted)
API base URL: https://p74uenx0qd.execute-api.eu-central-1.amazonaws.com (deleted)
CloudWatch log group: /aws/lambda/learning-notes-api (deleted)
```

## Files

```text
project-3-serverless-api/
  lambda_function.py
  events/
    create-note.json
    delete-note.json
    get-note.json
    list-notes.json
```

## Environment Variables

The Lambda reads the DynamoDB table name from:

```text
TABLE_NAME
```

If `TABLE_NAME` is not set, it defaults to:

```text
learning-notes
```

## Local Test Commands

Local tests call real AWS DynamoDB. Since the AWS resources have been deleted, these commands will fail unless the project is rebuilt first.

Use the SSO profile:

```bash
export AWS_PROFILE=aws-learning
export AWS_REGION=eu-central-1
export TABLE_NAME=learning-notes
```

Create a note:

```bash
python -c 'import json; import lambda_function as f; event=json.load(open("events/create-note.json")); print(json.dumps(f.lambda_handler(event, None), indent=2, ensure_ascii=False))'
```

List notes:

```bash
python -c 'import json; import lambda_function as f; event=json.load(open("events/list-notes.json")); print(json.dumps(f.lambda_handler(event, None), indent=2, ensure_ascii=False))'
```

For `get-note.json` and `delete-note.json`, replace `NOTE_ID` with an actual note id returned by the create command.

## HTTP API Examples

These examples are kept as a record of the deployed API shape. The API Gateway resource has been deleted, so the old URL no longer works unless rebuilt.

List notes:

```bash
curl https://p74uenx0qd.execute-api.eu-central-1.amazonaws.com/notes
```

Create a note:

```bash
curl -X POST https://p74uenx0qd.execute-api.eu-central-1.amazonaws.com/notes \
  -H 'content-type: application/json' \
  -d '{"title":"First API note","content":"Created through API Gateway."}'
```

Get one note:

```bash
curl https://p74uenx0qd.execute-api.eu-central-1.amazonaws.com/notes/NOTE_ID
```

Delete one note:

```bash
curl -X DELETE https://p74uenx0qd.execute-api.eu-central-1.amazonaws.com/notes/NOTE_ID
```

## Related Notes

See the Chinese learning note:

```text
../notes/05-project-3-serverless-api.md
```
