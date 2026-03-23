from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
import time

from tools.log_analyzer import get_pod_logs, list_pods
from tools.fix_suggester import suggest_fix
from tools.pipeline_trigger import trigger_workflow, get_workflow_status
from tools.metrics_fetcher import get_pod_restart_count, get_pod_memory_usage, get_pod_cpu_usage

load_dotenv()

@tool
def list_pods_tool(namespace: str) -> str:
    """Lists all pods in a Kubernetes namespace. Input: namespace name e.g. default or kube-system"""
    return str(list_pods(namespace))

@tool
def get_pod_logs_tool(pod_name: str) -> str:
    """Fetches logs from a specific Kubernetes pod. Input: pod name"""
    return get_pod_logs(pod_name=pod_name)

@tool
def suggest_fix_tool(error_context: str) -> str:
    """Analyzes error logs and suggests a fix using AI. Input: error message or log text"""
    return suggest_fix(error_context)

@tool
def get_workflow_status_tool(workflow_file: str) -> str:
    """Gets latest GitHub Actions workflow status. Input: workflow filename e.g. deploy.yml"""
    return get_workflow_status(workflow_file)

@tool
def trigger_workflow_tool(workflow_file: str) -> str:
    """Triggers a GitHub Actions workflow. Input: workflow filename e.g. deploy.yml"""
    return trigger_workflow(workflow_file)

@tool
def get_restart_count_tool(pod_name: str) -> str:
    """Gets restart count for a pod from Prometheus. Input: pod name"""
    return get_pod_restart_count(pod_name)

@tool
def get_memory_usage_tool(pod_name: str) -> str:
    """Gets memory usage for a pod from Prometheus. Input: pod name"""
    return get_pod_memory_usage(pod_name)

@tool
def get_cpu_usage_tool(pod_name: str) -> str:
    """Gets CPU usage for a pod from Prometheus. Input: pod name"""
    return get_pod_cpu_usage(pod_name)

# ── Setup LLM ───────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
    max_retries=3,
)

tools = [
    list_pods_tool,
    get_pod_logs_tool,
    suggest_fix_tool,
    get_workflow_status_tool,
    trigger_workflow_tool,
    get_restart_count_tool,
    get_memory_usage_tool,
    get_cpu_usage_tool,
]

agent = create_agent(llm, tools)

def run_agent(query: str):
    print(f"\n🤖 Agent Query: {query}")
    print("─" * 50)
    try:
        time.sleep(2)
        result = agent.invoke({
            "messages": [HumanMessage(content=query)]
        })
        final = result["messages"][-1].content
        print(f"\n✅ Final Answer:\n{final}")
        return final
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    run_agent("List all pods in default namespace")
