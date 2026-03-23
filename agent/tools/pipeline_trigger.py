import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def trigger_workflow(workflow_file: str = "deploy.yml", branch: str = "main") -> str:
    """
    Triggers a GitHub Actions workflow via API.
    """
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{workflow_file}/dispatches"

        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        payload = {"ref": branch}

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 204:
            return f"✅ Workflow '{workflow_file}' triggered successfully on branch '{branch}'"
        else:
            return f"❌ Failed to trigger workflow: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error triggering pipeline: {str(e)}"


def get_workflow_status(workflow_file: str = "deploy.yml") -> str:
    """
    Gets the latest run status of a GitHub Actions workflow.
    """
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{workflow_file}/runs"

        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if not data.get("workflow_runs"):
            return "No workflow runs found."

        latest = data["workflow_runs"][0]
        return (
            f"Latest run of '{workflow_file}':\n"
            f"  Status : {latest['status']}\n"
            f"  Result : {latest['conclusion']}\n"
            f"  Branch : {latest['head_branch']}\n"
            f"  Started: {latest['created_at']}"
        )

    except Exception as e:
        return f"Error fetching workflow status: {str(e)}"


# Quick test
if __name__ == "__main__":
    print("=== Workflow Status ===")
    print(get_workflow_status("deploy.yml"))
