# AWS AI Service Selection Table

| Scenario | Prefer | Why |
| --- | --- | --- |
| Summarize text | Bedrock | Open-ended generation |
| Ask questions over documents | Bedrock Knowledge Bases | Managed RAG |
| Agent calls backend tools | Bedrock Agents | Managed orchestration |
| Visual AI workflow | Bedrock Flows | Low-code AI workflow |
| Detect PII in text | Comprehend | Stable specialized NLP output |
| Translate text | Translate | Dedicated translation API |
| Extract text from scans or PDFs | Textract | OCR and document structure |
| Speech to text | Transcribe | Dedicated transcription API |
| Text to speech | Polly | Dedicated speech synthesis API |
| Image labels or moderation | Rekognition | Dedicated computer vision API |
| Train or package a Hugging Face model | SageMaker Training | Managed training compute |
| Deploy a Hugging Face model as an API | SageMaker Endpoint | Managed realtime model serving |
| Tune hyperparameters | SageMaker Hyperparameter Tuning | Managed HPO |
| Offline batch inference | SageMaker Batch Transform | No long-running endpoint |
| Realtime custom model inference | SageMaker Endpoint | Low-latency model serving |
| Model versioning and approval | SageMaker Model Registry | MLOps governance |
| Repeatable ML workflow | SageMaker Pipelines | MLOps automation |
| Monitor deployed model quality | SageMaker Model Monitor | Drift and quality monitoring |
