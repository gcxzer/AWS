# S3 Document Pipeline

An S3 ObjectCreated event can trigger Lambda when a document is uploaded to a specific prefix, such as documents/. Lambda reads the object from the input bucket, calls Bedrock Runtime to summarize it, and writes a summary JSON object to an output bucket.

Using separate input and output buckets avoids accidentally triggering Lambda recursively on files it writes itself.
