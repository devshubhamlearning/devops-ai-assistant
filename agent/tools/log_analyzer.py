from kubernetes import client, config
from dotenv import load_dotenv
import os

load_dotenv()

def load_k8s_config():
    """Load kubeconfig - works both locally and inside cluster."""
    try:
        # Try in-cluster config first (when running inside K8s)
        config.load_incluster_config()
    except Exception:
        # Fall back to local kubeconfig
        config.load_kube_config()

def get_pod_logs(namespace: str = "default", pod_name: str = None, lines: int = 50):
    try:
        load_k8s_config()
        v1 = client.CoreV1Api()
        if not pod_name:
            pods = v1.list_namespaced_pod(namespace=namespace)
            if not pods.items:
                return f"No pods found in namespace: {namespace}"
            pod_name = pods.items[0].metadata.name
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=lines
        )
        return f"Logs from pod '{pod_name}':\n{logs}"
    except Exception as e:
        return f"Error fetching logs: {str(e)}"


def list_pods(namespace: str = "default"):
    try:
        load_k8s_config()
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace=namespace)
        result = []
        for pod in pods.items:
            result.append({
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "namespace": namespace
            })
        return result if result else f"No pods in namespace: {namespace}"
    except Exception as e:
        return f"Error listing pods: {str(e)}"


if __name__ == "__main__":
    print("=== Listing Pods ===")
    pods = list_pods("kube-system")
    for p in pods:
        print(f"  {p['name']} → {p['status']}")
