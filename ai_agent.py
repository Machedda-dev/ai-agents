import subprocess
import json
import sys

def query_ollama(prompt, model="qwen2.5:7b"):
    """Send a prompt to Ollama and get a response"""
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',  # Fix the encoding issue
            errors='ignore',   # Ignore characters that can't be decoded
            timeout=180
        )
        return result.stdout.strip() if result.stdout else "No output received"
    except subprocess.TimeoutExpired:
        return "Error: Request timed out"
    except Exception as e:
        return f"Error: {str(e)}"

def analyse_logs(log_content):
    """Analyse logs using AI"""
    prompt = f"""
    Analyse this error and give 3 actionable fixes:
    Logs:
    {log_content[:500]}
    """
    return query_ollama(prompt)

def suggest_optimisations(health_data):
    """Suggest optimisations based on health data"""
    prompt = f"""
    Based on the following system health data, suggest 3-5 optimisations:

    {json.dumps(health_data, indent=2)[:1500]}
    """
    return query_ollama(prompt)

def chat(prompt):
    """Simple chat with the AI"""
    return query_ollama(prompt)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ai_agent.py chat 'your prompt here'")
        print("  python ai_agent.py analyse 'log content here'")
        sys.exit(1)

    command = sys.argv[1]
    if command == "chat":
        prompt = " ".join(sys.argv[2:])
        response = chat(prompt)
        print(response)
    elif command == "analyse":
        log_content = " ".join(sys.argv[2:])
        response = analyse_logs(log_content)
        print(response)
    else:
        print("Unknown command. Use 'chat' or 'analyse'.")