# Stage 8: Produktion, Kosten, IAM und Interview-Erklärung

## Ziel

In dieser Phase wird aus dem Lernprojekt eine saubere Projektgeschichte:

```text
Was habe ich gebaut?
Warum habe ich diese AWS Services benutzt?
Wie sichere ich das System?
Wie kontrolliere ich Kosten?
Wie überwache ich Fehler?
Wie erkläre ich das im Interview?
Wie räume ich Ressourcen wieder auf?
```

Stage 8 ist wichtig, weil viele Kandidaten nur sagen können:

```text
Ich habe S3, DynamoDB und Bedrock benutzt.
```

Besser ist:

```text
Ich kann Architektur, Security, Kosten, Fehlerfälle und Produktionsbetrieb erklären.
```

## Projektzusammenfassung

Projekt:

```text
AWS AI Document Assistant
```

Ziel:

```text
Benutzer laden Dokumente hoch.
Das System speichert Originaldateien, indexiert Textabschnitte, beantwortet Fragen mit RAG und kann später als Agent Tools aufrufen.
```

Architektur:

```text
User
  -> Application / API
      -> S3: raw documents
      -> DynamoDB: metadata + chat history
      -> OpenSearch: searchable chunks
      -> Bedrock: answer generation
      -> AgentCore: runtime, tools, memory, identity, observability
```

## Service-Rollen im Projekt

### S3

Rolle:

```text
Speichert Originaldateien.
```

Beispiel:

```text
s3://bucket/raw/user_001/sample.txt
```

Produktionsregeln:

- bucket nicht public machen
- default encryption aktivieren
- optional versioning
- lifecycle rules für alte Dateien
- presigned URLs nur kurzlebig
- keine dauerhaften öffentlichen Links

### DynamoDB

Rolle:

```text
Speichert Business Metadata und Chat History.
```

Tabellen:

```text
DocAssistantDocuments
partition key: user_id
sort key: document_id

DocAssistantChatMessages
partition key: session_id
sort key: created_at
```

Produktionsregeln:

- Zugriff über Query, nicht Scan
- key design nach access patterns
- status field nutzen: uploaded / indexing / indexed / failed
- TTL für temporäre Daten prüfen
- point-in-time recovery je nach Bedarf aktivieren
- keine riesigen Dokumenttexte in DynamoDB speichern

### OpenSearch

Rolle:

```text
Speichert searchable chunks und macht retrieval.
```

Index:

```text
document-chunks
```

Produktionsregeln:

- user_id filter bei jeder Suche erzwingen
- access control aktivieren
- public access vermeiden oder stark einschränken
- Kosten im Blick behalten
- logs und slow queries beobachten
- chunk size und search quality testen

### Bedrock

Rolle:

```text
Generiert Antworten aus Frage + retrieved context.
```

Produktionsregeln:

- maxTokens begrenzen
- temperature niedrig halten für RAG
- nicht ganze Dokumente in Prompt stecken
- nur top-k chunks verwenden
- Fehler behandeln: AccessDenied, Validation, Throttling, Timeout
- Kosten nach input/output tokens beobachten

### AgentCore

Rolle:

```text
Macht aus dem festen RAG Flow einen produktionsfähigen Agent mit Tools, Memory, Identity und Observability.
```

Module:

```text
Runtime
führt Agent-Code aus

Gateway
stellt Tools bereit

Memory
speichert Kontext und langfristige Erinnerung

Identity
verwaltet User-/Agent-Identität und Credentials

Observability
zeigt Logs, Metrics und Traces
```

## Produktionsarchitektur

Eine realistische Produktionsversion:

```text
Browser / Client
  -> CloudFront
  -> API Gateway
  -> Lambda / ECS / AgentCore Runtime
      |-- S3
      |-- DynamoDB
      |-- OpenSearch
      |-- Bedrock
      |-- AgentCore Gateway / Memory / Identity
  -> CloudWatch / Observability
```

Warum CloudFront?

```text
globaler Einstiegspunkt
HTTPS
Caching statischer Assets
WAF möglich
```

Warum API Gateway?

```text
API Routing
Auth
Throttling
Stages: dev/prod
```

Warum private Backends?

```text
S3 bleibt private
DynamoDB wird nicht direkt vom Browser angesprochen
OpenSearch nicht öffentlich ohne Schutz
Bedrock wird nur serverseitig aufgerufen
```

## IAM: Least Privilege

IAM-Grundsatz:

```text
Gib nur die Rechte, die wirklich gebraucht werden.
```

Nicht gut:

```text
AdministratorAccess für die App
```

Gut:

```text
separate IAM role für die App / Agent Runtime
nur konkrete Aktionen auf konkrete Ressourcen
```

### Beispiel App Role Rechte

S3:

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::YOUR_BUCKET/raw/*"
}
```

DynamoDB:

```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:Query"
  ],
  "Resource": [
    "arn:aws:dynamodb:REGION:ACCOUNT:table/DocAssistantDocuments",
    "arn:aws:dynamodb:REGION:ACCOUNT:table/DocAssistantChatMessages"
  ]
}
```

Bedrock:

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeModel",
    "bedrock:InvokeModelWithResponseStream"
  ],
  "Resource": "arn:aws:bedrock:REGION::foundation-model/MODEL_ID"
}
```

OpenSearch:

```text
Erlaubnis nur für benötigte index/search APIs.
Zusätzlich OpenSearch access control / fine-grained access control konfigurieren.
```

CloudWatch:

```json
{
  "Effect": "Allow",
  "Action": [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ],
  "Resource": "*"
}
```

In Produktion kann man auch CloudWatch Resources einschränken.

## Security Checklist

### S3

- [ ] Block Public Access aktiv
- [ ] Default encryption aktiv
- [ ] keine öffentlichen Bucket Policies
- [ ] presigned URLs kurzlebig
- [ ] object keys nach user prefix getrennt
- [ ] keine Secrets in object metadata

### DynamoDB

- [ ] Query statt Scan
- [ ] user_id als Zugriffskontrollgrenze beachten
- [ ] keine sensiblen Secrets speichern
- [ ] optional PITR aktivieren
- [ ] TTL für temporäre Daten prüfen

### OpenSearch

- [ ] kein ungeschützter Public Access
- [ ] fine-grained access control aktiv
- [ ] user_id filter in jeder Query
- [ ] keine fremden user chunks zurückgeben
- [ ] slow logs / audit logs prüfen
- [ ] domain nach Lernphase löschen, wenn nicht gebraucht

### Bedrock

- [ ] Modellzugriff bewusst gewählt
- [ ] maxTokens begrenzt
- [ ] keine sensiblen Daten in unnötige Prompts
- [ ] retry/backoff für Throttling
- [ ] Fehler sauber melden

### AgentCore

- [ ] Tools klein und klar definiert
- [ ] Gateway Auth konfiguriert
- [ ] Identity-Kontext statt user_id aus Prompt
- [ ] Memory speichert keine Secrets
- [ ] Observability ohne private Volltexte
- [ ] Tool calls auditierbar

## Kostenkontrolle

Wichtige Kostenquellen:

```text
S3
Speicher + Requests

DynamoDB
On-demand Reads/Writes

OpenSearch
Domain / Instance Hours / EBS / OCU bei Serverless

Bedrock
Input Tokens + Output Tokens

AgentCore
Runtime / Gateway / Memory / Observability je nach Nutzung

CloudWatch
Logs, Metrics, Traces
```

### Budget

Immer setzen:

```text
AWS Budget
Monthly cost budget: 10-20 USD für Lernphase
Alerts: 50%, 80%, 100%
```

### Was ist in diesem Projekt teuer?

Meistens:

```text
OpenSearch
Bedrock token usage
CloudWatch logs bei viel Traffic
```

S3 und DynamoDB sind bei kleinen Lernmengen meist günstig.

### Kostenregeln

- OpenSearch nur erstellen, wenn wirklich gebraucht
- OpenSearch nach Übung löschen
- Bedrock `maxTokens` begrenzen
- nur top 3-5 chunks in Prompt
- Chat History kürzen
- keine Endlosschleifen bei Agents
- CloudWatch log retention setzen
- cleanup checklist pflegen

## Cleanup Checklist

Nach Lern- oder Demo-Phase prüfen:

### S3

```text
aws-ai-doc-assistant-* buckets
objects löschen
bucket löschen
```

### DynamoDB

```text
DocAssistantDocuments
DocAssistantChatMessages
```

löschen, wenn nicht mehr gebraucht.

### OpenSearch

```text
doc-assistant-dev domain
document-chunks index
serverless collections
security policies
network policies
encryption policies
```

löschen, wenn nicht mehr gebraucht.

### Bedrock

Bedrock hat oft keine dauerhafte Ressource für reine Modellaufrufe.

Aber prüfen:

```text
custom model jobs
provisioned throughput
evaluation jobs
guardrails
knowledge bases
agents
```

falls genutzt.

### AgentCore

Prüfen:

```text
Runtime resources
Gateway resources
Gateway targets
Memory resources
Identity credential providers
CloudWatch log groups
```

### CloudWatch

Prüfen:

```text
log groups
retention policy
metrics
traces
alarms
```

## Observability Plan

Für Produktion loggen:

```text
request_id
session_id
actor_id
tool_name
duration_ms
result_count
chunk_ids
model_id
input_tokens
output_tokens
error_type
status
```

Nicht loggen:

```text
passwords
AWS access keys
OAuth tokens
full presigned URLs
vollständige private Dokumente
unnötige personenbezogene Daten
```

Wichtige Metriken:

```text
requests per minute
error rate
p50/p95 latency
OpenSearch retrieval latency
Bedrock latency
token usage
tool call count
empty retrieval rate
answer with sources rate
```

## Fehlerbehandlung

### User-freundliche Fehler

Nicht:

```text
botocore.exceptions.ClientError: AccessDeniedException...
```

Besser:

```text
Ich kann dieses Dokument aktuell nicht abrufen. Bitte versuche es später erneut.
```

Intern trotzdem loggen:

```text
error_type
service
request_id
resource
```

### Retry Regeln

Retry bei:

```text
Throttling
Timeout
temporären 5xx Fehlern
```

Kein Retry bei:

```text
AccessDenied
ValidationException
NoSuchKey
falscher model_id
```

## Interview-Erklärung Kurzversion

Deutsch:

```text
Ich habe einen AWS AI Document Assistant entworfen.

Originaldokumente werden in S3 gespeichert. DynamoDB speichert die Dokument-Metadaten, den Verarbeitungsstatus und Chat History. Die Dokumente werden in Chunks geteilt und in OpenSearch indexiert, damit das System relevante Textstellen finden kann. Bei einer Nutzerfrage sucht OpenSearch zuerst passende Chunks, dann generiert Bedrock aus diesen Chunks eine Antwort.

In der erweiterten Version werden die Funktionen wie Dokumentensuche, Chat-History-Abfrage und Download-Link-Erzeugung als Tools modelliert. Mit Bedrock AgentCore kann daraus ein Agent werden, der über Runtime, Gateway, Memory, Identity und Observability produktionsfähig betrieben wird.
```

Englisch:

```text
I designed an AWS AI document assistant.

Raw documents are stored in S3. DynamoDB stores document metadata, processing status, and chat history. Document text is split into chunks and indexed in OpenSearch for retrieval. When a user asks a question, OpenSearch retrieves the most relevant chunks and Bedrock generates an answer grounded in that context.

In the agentic version, capabilities such as document search, chat history lookup, metadata retrieval, and presigned URL generation are exposed as tools. Bedrock AgentCore can run the agent with Runtime, Gateway, Memory, Identity, and Observability for production use.
```

## Interview-Erklärung Detailversion

Wenn der Interviewer fragt:

```text
Warum S3?
```

Antwort:

```text
S3 ist ideal für Originaldateien und unstrukturierte Daten. Es ist langlebig, günstig für Speicherung und unterstützt Verschlüsselung, Lifecycle Rules und presigned URLs. Ich würde private Buckets verwenden und Downloads nur über kurzlebige presigned URLs erlauben.
```

Wenn gefragt wird:

```text
Warum DynamoDB?
```

Antwort:

```text
DynamoDB speichert strukturierte Business-Daten wie user_id, document_id, s3_uri, status und Chat History. Ich designe die Tabellen nach Zugriffsmustern: user_id + document_id für Dokumente und session_id + created_at für Chat Messages. So kann ich Query statt Scan verwenden.
```

Wenn gefragt wird:

```text
Warum OpenSearch?
```

Antwort:

```text
OpenSearch ist die Retrieval-Schicht. Es speichert Dokument-Chunks und kann relevante Textstellen per Volltextsuche oder später per Vektorsuche finden. S3 speichert nur Dateien und DynamoDB ist keine Volltextsuchmaschine, deshalb brauche ich OpenSearch für semantisch oder keyword-basierte Suche.
```

Wenn gefragt wird:

```text
Warum Bedrock?
```

Antwort:

```text
Bedrock stellt Foundation Models über AWS bereit. Ich muss keine Modelle selbst hosten und kann über APIs wie Converse Antworten erzeugen. Im RAG-System bekommt Bedrock nicht die ganze Datei, sondern nur die relevanten Chunks aus OpenSearch.
```

Wenn gefragt wird:

```text
Was bringt AgentCore?
```

Antwort:

```text
AgentCore macht den Agent produktionsfähig. Runtime hostet den Agent, Gateway stellt Tools bereit, Memory verwaltet Kontext, Identity kontrolliert wer auf welche Daten zugreift, und Observability zeigt Tool Calls, Latenz und Fehler. Damit wird aus einem festen RAG Flow ein sicherer, beobachtbarer Agent mit Tool Calling.
```

## Typische Interviewfragen

### S3 vs DynamoDB

```text
S3 speichert Objekte und Dateien.
DynamoDB speichert strukturierte Items für schnelle key-basierte Abfragen.
```

### DynamoDB Query vs Scan

```text
Query nutzt partition key und optional sort key.
Scan liest die ganze Tabelle.
Bei großen Tabellen ist Scan teuer und langsam.
```

### OpenSearch Keyword vs Vector Search

```text
Keyword search nutzt inverted index und BM25.
Vector search nutzt embeddings und Ähnlichkeitssuche.
Für RAG ist hybrid search oft stark: keyword + vector.
```

### Wie schützt du private Dokumente?

```text
Private S3 bucket, keine public access policies, presigned URLs mit kurzer Laufzeit, user_id Filter in DynamoDB und OpenSearch, IAM least privilege und AgentCore Identity.
```

### Wie debuggt man schlechte RAG-Antworten?

Reihenfolge:

```text
1. Wurden relevante chunks gefunden?
2. Waren die chunks im Prompt?
3. War der Prompt klar?
4. Hat das Modell Quellen genutzt?
5. War die Frage zu unklar?
6. Braucht man bessere chunking strategy oder vector search?
```

### Wie kontrollierst du Kosten?

```text
Budget alerts, kleine Lernressourcen, OpenSearch nach Tests löschen, maxTokens begrenzen, nur top-k chunks verwenden, CloudWatch log retention setzen und cleanup scripts nutzen.
```

## Projekt-README Struktur

Ein gutes README sollte haben:

```text
1. Projektziel
2. Architekturdiagramm
3. Services und Rollen
4. Setup
5. Demo Flow
6. Kostenhinweise
7. Cleanup
8. Sicherheitsannahmen
9. Erweiterungen
```

## Realistische Verbesserungen

Nach dem Grundprojekt:

- PDF parsing
- Textract für Scans
- OpenSearch vector search
- hybrid search
- reranking
- citations mit page number
- user authentication
- CloudFront + API Gateway frontend
- AgentCore Gateway tools
- AgentCore Memory
- Guardrails
- evaluation dataset
- CI/CD
- least privilege IAM

## Realistische Grenzen

Nicht behaupten:

```text
Das System ist sofort enterprise-ready.
```

Besser:

```text
Das Projekt zeigt eine realistische Architektur und die wichtigsten Produktionsaspekte. Für Enterprise-Betrieb würde ich zusätzlich Auth, IAM least privilege, observability, evaluation, backup, data retention und compliance genauer ausarbeiten.
```

## Bereits durchgeführte Cleanup-Aktion

### 2026-05-06

- AWS Lernressourcen aus den ersten Übungen wurden gelöscht
- Gelöschter S3 bucket: `aws-ai-doc-assistant-xzhu-089781651608-eu-central-1-an`
- Gelöschte DynamoDB Tabelle: `DocAssistantDocuments`
- Gelöschte DynamoDB Tabelle: `DocAssistantChatMessages`
- Es existierte kein OpenSearch domain mit Prefix `doc-assistant*`
- Es existierte keine OpenSearch Serverless collection mit Prefix `doc-assistant*`
- TopicFollow oder andere bestehende Projektressourcen wurden nicht gelöscht

## Fertigstellungskriterien

- [x] Architektur kann erklärt werden
- [x] Service-Rollen sind klar
- [x] IAM Least Privilege ist verstanden
- [x] Kostenquellen sind bekannt
- [x] Cleanup Checklist ist vorhanden
- [x] Observability Plan ist vorhanden
- [x] Security Checklist ist vorhanden
- [x] Interview-Erklärung auf Deutsch und Englisch ist vorhanden
- [x] Typische Interviewfragen sind vorbereitet

## Nächste Schritte

Wenn daraus ein Portfolio-Projekt werden soll:

1. README im Root-Projekt finalisieren
2. Architekturdiagramm erstellen
3. Demo Flow mit Screenshots dokumentieren
4. Cleanup Script schreiben
5. Eine kleine RAG-Demo lokal oder mit echten AWS Ressourcen neu aufbauen
6. GitHub Repo / PR / Projektbeschreibung vorbereiten
