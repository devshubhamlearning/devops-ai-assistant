from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

def suggest_fix(error_context: str) -> str:
    """
    Takes error logs or incident description,
    returns AI-suggested fix.
    """
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )

        messages = [
            SystemMessage(content="""You are an expert DevOps engineer. 
            Analyze the given error or log and provide:
            1. Root Cause (1-2 lines)
            2. Immediate Fix (step by step)
            3. Long-term Prevention
            Be concise and practical."""),

            HumanMessage(content=f"""
            Here is the error/log to analyze:
            
            {error_context}
            
            Provide your analysis and fix suggestion.
            """)
        ]

        response = llm.invoke(messages)
        return response.content

    except Exception as e:
        return f"Error calling LLM: {str(e)}"


# Quick test
if __name__ == "__main__":
    sample_error = """
    Error: OOMKilled - Container 'app' in pod 'web-app-xyz' 
    was killed due to Out Of Memory.
    Last restart count: 5
    Memory limit: 256Mi
    """

    print("=== AI Fix Suggestion ===")
    result = suggest_fix(sample_error)
    print(result)
