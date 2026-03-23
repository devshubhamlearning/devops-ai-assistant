from main import run_agent
import sys

def main():
    print("""
╔══════════════════════════════════════════╗
║       🤖 DevOps AI Assistant CLI        ║
║  Type your query or 'exit' to quit      ║
╚══════════════════════════════════════════╝

Example queries:
  → List all pods in default namespace
  → Get health report for pod <pod-name>
  → Fetch logs from pod <pod-name>
""")

    while True:
        try:
            query = input("🔵 You: ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit", "q"]:
                print("👋 Goodbye!")
                sys.exit(0)
            run_agent(query)
            print()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
