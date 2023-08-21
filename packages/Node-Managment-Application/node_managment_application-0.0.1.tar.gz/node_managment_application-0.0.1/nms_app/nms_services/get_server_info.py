import requests
import platform
import psutil
import os


def get_open_ports():
    open_ports = []
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN':
            open_ports.append(str(conn.laddr.port))
    return open_ports


def bytes_to_GB(bytes):
    gb = bytes / (1024 * 1024 * 1024)
    gb = round(gb, 2)
    return gb


def get_server_info():
    try:
        location_response = requests.get(f"http://ip-api.com/json")
        location_data = location_response.json()
        # Extracting relevant information
        server_ip = location_data['query']
        server_location = f"{location_data['city']}, {location_data['regionName']}, {location_data['country']}"

        return server_ip, server_location

    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)


def get_server_details():
    # importing the required modules

    with open("/proc/uptime", "r") as f:
        uptime = f.read().split(" ")[0].strip()

    cpufreq = psutil.cpu_freq()

    # Using the virtual_memory() function it will return a tuple
    virtual_memory = psutil.virtual_memory()

    uptime = int(float(uptime))
    uptime_hours = uptime // 3600
    uptime_minutes = (uptime % 3600) // 60

    return {"architecture": platform.architecture()[0],
            "machine": platform.machine(),
            "operating_system_release": platform.release(),
            "system_name": platform.system(),
            "operating_system_version": platform.version(),
            "node": platform.node(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "system_uptime": str(uptime_hours) + " hours " + str(uptime_minutes) + " min",
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "max_frequency": f"{cpufreq.max:.2f}Mhz",
            "min_frequency": f"{cpufreq.min:.2f}Mhz",
            "current_frequency": f"{cpufreq.current:.2f}Mhz",
            "total_cpu_usage": f"{psutil.cpu_percent()}%",
            "total_ram_memory_present": str(bytes_to_GB(virtual_memory.total)) + "Gb",
            "total_ram_memory_available": str(bytes_to_GB(virtual_memory.available)) + "Gb",
            "total_ram_memory_used": str(bytes_to_GB(virtual_memory.used)) + "Gb",
            "ram_percentage_used": str(virtual_memory.percent) + "%",
            "total_memery": f"{bytes_to_GB(psutil.disk_usage(os.sep).total)} GB",
            "used_memery": f"{bytes_to_GB(psutil.disk_usage(os.sep).used)} GB",
            "free_memery": f"{bytes_to_GB(psutil.disk_usage(os.sep).free)} GB",
            "used_memery_in_percentage": f"{psutil.disk_usage(os.sep).percent} %"}
