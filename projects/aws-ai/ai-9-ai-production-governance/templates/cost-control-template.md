# AI Cost Control Template

## Budget

| Item | Value |
| --- | --- |
| Monthly learning budget |  |
| Alert threshold 1 | 50% |
| Alert threshold 2 | 80% |
| Alert threshold 3 | 100% |
| Notification target |  |

## Cost Drivers

| Component | Cost driver | Control |
| --- | --- | --- |
| Bedrock model | input/output tokens or model-specific unit | cap input/output, choose smaller model |
| Agents | orchestration model calls and tool calls | limit turns, inspect trace |
| Knowledge Bases | embedding, vector store, retrieval, generation | small docs, cleanup vector store |
| Guardrails | guardrail checks | short text, apply where needed |
| Flows | underlying node calls | keep minimal, avoid accidental loops |
| Evaluations | generator and judge models, S3 | tiny datasets |
| Lambda | duration and requests | timeout, memory, no retry storms |
| CloudWatch Logs | stored log volume | retention policy, no raw large prompts |
| S3 | storage and requests | delete test data |

## Required Tags

```text
Project=AWS-AI-Learning
Stage=dev
Owner=xzhu
TTL=manual-cleanup
```

## Pre-Experiment Cost Gate

- [ ] Know which services will be created.
- [ ] Know which services can keep charging after the test.
- [ ] Know how to delete them.
- [ ] Use smallest useful dataset.
- [ ] Avoid load testing.
- [ ] Record cleanup result in notes.
