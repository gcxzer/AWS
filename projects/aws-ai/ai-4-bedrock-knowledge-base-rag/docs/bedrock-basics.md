# Bedrock Basics

Amazon Bedrock is a managed AWS service for building generative AI applications with foundation models. Application code calls Bedrock Runtime to run inference. AWS IAM controls which role can invoke which model.

In earlier AI learning projects, a local Python script used boto3 to call Bedrock Runtime, and a Lambda function used its execution role to call Bedrock from a serverless API.
