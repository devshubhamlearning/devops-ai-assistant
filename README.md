# 🤖 DevOps AI Assistant 

An **Agentic AI DevOps Assistant** that autonomously monitors Kubernetes clusters, fetches logs, analyzes metrics from Prometheus, and suggests fixes using LLMs.

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────┐
│              DevOps AI Agent                 │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Log    │  │ Metrics  │  │   Fix    │  │
│  │Analyzer  │  │ Fetcher  │  │Suggester │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │              │              │        │
│       ▼              ▼              ▼        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Kubernetes│  │Prometheus│  │  Groq    │  │
│  │  API     │  │  API     │  │  LLM     │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
```

---

## 🚀 Features

- ✅ **Live K8s Pod Monitoring** — list pods and fetch real-time logs
- ✅ **Prometheus Metrics** — restart counts, memory and CPU usage
- ✅ **AI Root Cause Analysis** — LLM diagnoses errors and suggests fixes
- ✅ **Dockerized** — runs as a container inside KIND cluster
- ✅ **RBAC secured** — uses ServiceAccount with minimal permissions

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core language |
| LangChain | Agent framework |
| Groq (LLaMA 3.3) | LLM inference |
| Kubernetes | Container orchestration |
| Prometheus | Metrics collection |
| Docker | Containerization |
| KIND | Local K8s cluster |
| GitHub Actions | CI/CD |

---

## ⚙️ Local Setup

### Prerequisites
- WSL2 / Linux / Mac
- Docker
- KIND
- kubectl
- Python 3.10+

### Install
```bash
# Clone the repo
git clone git@github.com:YOUR_USERNAME/devops-ai-assistant.git
cd devops-ai-assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Create KIND cluster
```bash
kind create cluster --name devops-ai
```

### Deploy Prometheus
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --set server.persistentVolume.enabled=false
```

### Run locally
```bash
cd agent
python3 main.py
```

### Deploy to KIND
```bash
docker build -t devops-ai-agent:latest -f docker/Dockerfile .
kind load docker-image devops-ai-agent:latest --name devops-ai
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/agent-deployment.yaml
```

---

## 🧪 Demo
```bash
# Run full diagnosis on a pod
cd agent
python3 -c "
from tools.log_analyzer import get_pod_logs
from tools.metrics_fetcher import get_full_pod_health
from tools.fix_suggester import suggest_fix

pod = 'your-pod-name'
health = get_full_pod_health(pod)
logs = get_pod_logs(pod_name=pod)
fix = suggest_fix(f'{health}\n\nLogs:\n{logs}')
print(health)
print(fix)
"
```

---

## 📁 Project Structure
```
devops-ai-assistant/
├── agent/
│   ├── main.py                    # LangChain agent entry point
│   └── tools/
│       ├── log_analyzer.py        # K8s log fetcher
│       ├── fix_suggester.py       # AI fix suggester
│       ├── metrics_fetcher.py     # Prometheus metrics
│       └── pipeline_trigger.py   # GitHub Actions trigger
├── k8s/
│   ├── agent-deployment.yaml     # Agent K8s deployment
│   ├── rbac.yaml                 # ServiceAccount + RBAC
│   └── broken-app.yaml           # Sample broken app for testing
├── docker/
│   └── Dockerfile
├── monitoring/
│   └── prometheus.yaml
├── .github/
│   └── workflows/
│       └── deploy.yml
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🔐 GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `GROQ_API_KEY` | Your Groq API key |

---

## 💡 Problem → Solution → Impact

**Problem:** Kubernetes incidents require manual log analysis, metric correlation, and fix research — taking 30-60 mins per incident.

**Solution:** AI agent that autonomously fetches logs + metrics and provides root cause analysis in seconds.

**Impact:** Reduced incident response time from ~45 mins to ~30 seconds.
