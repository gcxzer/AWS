# AI-8 Manual RAG Evaluation Scorecard

Use this scorecard when you want to evaluate RAG or model responses before creating a full Bedrock Evaluation job.

Scoring:

| Score | Meaning |
| --- | --- |
| 0 | Incorrect or unsupported |
| 1 | Partially correct, important gaps |
| 2 | Mostly correct, minor gaps |
| 3 | Correct, grounded, and complete |

## Fields

| Field | Meaning |
| --- | --- |
| `retrieval_hit` | Did retrieval find the expected source? |
| `answer_correctness` | Did the answer address the question correctly? |
| `source_grounding` | Is the answer supported by retrieved content? |
| `missing_points` | What key facts were missing? |
| `score` | 0-3 overall score |
| `notes` | Reviewer notes |

## Scorecard

This filled table is a reference-answer baseline. It assumes the answer being reviewed matches the expected answer in `datasets/aws-ai-rag-eval.jsonl`. When reviewing a real RAG or model response, replace these scores with the actual review result.

| ID | Question | Expected source | Retrieval hit | Answer correctness | Source grounding | Missing points | Score | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ai8-001 | What is the difference between Bedrock model access and IAM permissions? | `notes/aws-ai/01-bedrock-call-and-permissions.md` | yes | 3 | 3 | none | 3 | Correctly separates account/Region model access from IAM API authorization. |
| ai8-002 | Why should a browser frontend not call Bedrock directly? | `notes/aws-ai/02-bedrock-serverless-api.md` | yes | 3 | 3 | none | 3 | Correctly covers credential exposure, backend validation, cost control, model choice, logging, and Lambda execution role boundary. |
| ai8-003 | How does the S3 AI document pipeline work? | `notes/aws-ai/03-s3-ai-document-pipeline.md` | yes | 3 | 3 | none | 3 | Correctly describes S3 ObjectCreated, Lambda processing, Bedrock call, output write, and traceable failure path. |
| ai8-004 | What is the difference between Retrieve and RetrieveAndGenerate in a Bedrock Knowledge Base? | `notes/aws-ai/04-bedrock-knowledge-base-rag.md` | yes | 3 | 3 | none | 3 | Correctly separates source-chunk retrieval from retrieval plus generated answer and citations. |
| ai8-005 | In Bedrock Agents, what is the difference between an action schema and a Lambda tool? | `notes/aws-ai/05-bedrock-agent-lambda-tool.md` | yes | 3 | 3 | none | 3 | Correctly explains schema as tool description and Lambda as deterministic executor returning the Agent response envelope. |
| ai8-006 | Why are Guardrails not a replacement for IAM or application authorization? | `notes/aws-ai/06-bedrock-guardrails.md` | yes | 3 | 3 | none | 3 | Correctly distinguishes content safety from AWS resource permissions and business authorization. |
| ai8-007 | How is a Bedrock Flow different from a Bedrock Agent? | `notes/aws-ai/07-bedrock-flows.md` | yes | 3 | 3 | none | 3 | Correctly identifies Flow as explicit node-based workflow and Agent as model-driven dynamic decision making. |

Baseline average score:

```text
3.0 / 3.0
```

## Review Questions

For each answer, ask:

1. Did retrieval find the right source document?
2. Did the answer include the key expected facts?
3. Did the answer add unsupported claims?
4. Would the answer help an engineer make the right AWS design decision?
5. What should change: documents, chunking, top_k, prompt, or model?
