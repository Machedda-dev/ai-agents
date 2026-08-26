import json
from datetime import datetime
from monitor_agent import get_system_health
from ai_agent import query_ollama

def generate_report():
    print("=" * 50)
    print("     SYSTEM HEALTH REPORT WITH AI ANALYSIS")
    print("=" * 50)
    print(f"Generated: {datetime.now().isoformat()}")
    print("-" * 50)
    
    # Collect system health data
    health = get_system_health()
    
    # Display metrics
    cpu = health.get('cpu', 'N/A')
    mem = health.get('memory', 'N/A')
    disk = health.get('disk', [])
    
    print("SYSTEM METRICS:")
    print(f"  CPU Load: {cpu}%")
    if mem != "N/A":
        print(f"  Memory Used: {mem.get('used', 'N/A')}GB / {mem.get('total', 'N/A')}GB")
        print(f"  Memory Free: {mem.get('free', 'N/A')}GB")
    print("  Disk:")
    for d in disk:
        print(f"    {d.get('drive')}: {d.get('free')}GB free / {d.get('total')}GB total")
    print("-" * 50)
    
    # Build AI prompt
    prompt = f"""
    Based on this system health data, suggest 3 optimisations:
    CPU Load: {cpu}%
    Memory: {mem}
    Disk Info: {json.dumps(disk, indent=2)}
    """
    
    # Get AI analysis
    print("AI ANALYSIS:")
    analysis = query_ollama(prompt)
    print(analysis)
    print("-" * 50)
    
    # Save report
    report_path = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w") as f:
        json.dump(health, f, indent=2)
    print(f"Report saved to: {report_path}")
    print("=" * 50)

if __name__ == "__main__":
    generate_report()