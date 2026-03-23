from kubernetes import client, config
from dotenv import load_dotenv
import os

load_dotenv()

def get_pod_logs(namespace: str = "default", pod_name: str = None, lines: int = 50):
    """
    Fetches logs from a Kubernetes pod.
    If no pod_name given, fetches from first pod in namespace.
    """
    try:
        # Load kubeconfig (works locally with KIND)
        config.load_kube_config()

        v1 = client.CoreV1Api()

        # If no pod name provided, pick the first one
        if not pod_name:
            pods = v1.list_namespaced_pod(namespace=namespace)
            if not pods.items:
                return f"No pods found in namespace: {namespace}"
            pod_name = pods.items[0].metadata.name

        # Fetch logs
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=lines
        )

        return f"Logs from pod '{pod_name}':\n{logs}"

    except Exception as e:
        return f"Error fetching logs: {str(e)}"


def list_pods(namespace: str = "default"):
    """
    Lists all pods in a namespace with their status.
    """
    try:
        config.load_kube_config()
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


# Quick test
if __name__ == "__main__":
    print("=== Listing Pods ===")
    pods = list_pods("kube-system")
    for p in pods:
        print(f"  {p['name']} → {p['status']}")
