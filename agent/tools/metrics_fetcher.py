import requests
import os
from dotenv import load_dotenv

load_dotenv()

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")

def query_prometheus(query: str):
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": query},
            timeout=10
        )
        data = response.json()
        if data["status"] != "success":
            return f"Prometheus query failed: {data}"
        return data["data"]["result"]
    except Exception as e:
        return f"Error querying Prometheus: {str(e)}"


def get_pod_restart_count(pod_name: str, namespace: str = "default") -> str:
    query = f'kube_pod_container_status_restarts_total{{pod="{pod_name}",namespace="{namespace}"}}'
    results = query_prometheus(query)
    if isinstance(results, str):
        return results
    for r in results:
        if r["metric"].get("pod") == pod_name:
            return f"⚠️  Pod '{pod_name}' has restarted {r['value'][1]} times!"
    return f"No restart data found for {pod_name}"


def get_pod_memory_usage(pod_name: str, namespace: str = "default") -> str:
    query = f'container_memory_usage_bytes{{pod="{pod_name}",namespace="{namespace}"}}'
    results = query_prometheus(query)
    if isinstance(results, str):
        return results
    output = []
    for r in results:
        # get container name from multiple possible label keys
        container = (
            r["metric"].get("container") or
            r["metric"].get("name") or
            r["metric"].get("image", "unknown").split("/")[-1]
        )
        bytes_used = int(r["value"][1])
        mb_used = round(bytes_used / (1024 * 1024), 2)
        output.append(f"  Container '{container}': {mb_used} MB")
    return f"Memory usage for '{pod_name}':\n" + "\n".join(output) if output else "No memory data found"


def get_pod_cpu_usage(pod_name: str, namespace: str = "default") -> str:
    # Try multiple queries — cadvisor sometimes needs different filters
    queries = [
        f'rate(container_cpu_usage_seconds_total{{pod="{pod_name}",namespace="{namespace}"}}[5m])',
        f'irate(container_cpu_usage_seconds_total{{pod="{pod_name}"}}[5m])',
        f'container_cpu_usage_seconds_total{{pod="{pod_name}"}}'
    ]
    for query in queries:
        results = query_prometheus(query)
        if isinstance(results, list) and results:
            output = []
            for r in results:
                container = (
                    r["metric"].get("container") or
                    r["metric"].get("name") or
                    r["metric"].get("id", "unknown").split("/")[-1][:20]
                )
                cpu = round(float(r["value"][1]) * 100, 4)
                output.append(f"  Container '{container}': {cpu}% CPU")
            return f"CPU usage for '{pod_name}':\n" + "\n".join(output)
    return "No CPU data found"


def get_full_pod_health(pod_name: str, namespace: str = "default") -> str:
    """Get complete health summary of a pod."""
    restarts = get_pod_restart_count(pod_name, namespace)
    memory = get_pod_memory_usage(pod_name, namespace)
    cpu = get_pod_cpu_usage(pod_name, namespace)
    return f"""
🔍 Health Report for '{pod_name}':
{'─'*40}
{restarts}
{memory}
{cpu}
{'─'*40}
"""

if __name__ == "__main__":
    pod = "broken-app-7745479d67-cwrjh"
    print(get_full_pod_health(pod))
