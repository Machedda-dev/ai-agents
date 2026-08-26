import subprocess
import json
from datetime import datetime

def get_system_health():
    """Collect system health metrics"""
    health = {
        "timestamp": datetime.now().isoformat(),
        "cpu": get_cpu_usage(),
        "memory": get_memory_usage(),
        "disk": get_disk_usage(),
        "services": get_service_status()
    }
    return health

def get_cpu_usage():
    try:
        result = subprocess.run(["wmic", "cpu", "get", "loadpercentage"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        return lines[1].strip() if len(lines) > 1 else "N/A"
    except:
        return "N/A"

def get_memory_usage():
    try:
        result = subprocess.run(["wmic", "OS", "get", "FreePhysicalMemory,TotalVisibleMemorySize"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:
            parts = lines[1].split()
            free = int(parts[0]) / 1024
            total = int(parts[1]) / 1024
            used = total - free
            return {"total": round(total, 2), "used": round(used, 2), "free": round(free, 2)}
        return "N/A"
    except:
        return "N/A"

def get_disk_usage():
    try:
        result = subprocess.run(["wmic", "logicaldisk", "where", "drivetype=3", "get", "deviceid,size,freespace"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        disks = []
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    disks.append({
                        "drive": parts[0],
                        "total": round(int(parts[1]) / 1e9, 2),
                        "free": round(int(parts[2]) / 1e9, 2)
                    })
        return disks
    except:
        return []

def get_service_status():
    try:
        result = subprocess.run(["sc", "query", "state=all"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        services = []
        for line in lines:
            if "SERVICE_NAME" in line:
                name = line.split(":")[1].strip()
            elif "STATE" in line:
                state = line.split(":")[1].strip().split()[0]
                services.append({"name": name, "state": state})
        return services
    except:
        return []

if __name__ == "__main__":
    health = get_system_health()
    print(json.dumps(health, indent=2))