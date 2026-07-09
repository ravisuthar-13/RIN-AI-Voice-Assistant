import psutil
import shutil

def get_battery_status():
    battery = psutil.sensors_battery()

    if battery is None:
        return "Sorry buddy, I can't read the battery."

    percent = int(battery.percent)
    plugged = battery.power_plugged

    if plugged:
        if percent >= 95:
            return f"Battery is {percent} percent and fully charged buddy."
        else:
            return f"Battery is {percent} percent and charging."

    if percent <= 20:
        return f"Buddy, battery is only {percent} percent. Please connect your charger."

    elif percent <= 40:
        return f"Battery is {percent} percent. You may want to charge it soon."

    else:
        return f"Battery is {percent} percent."

def get_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)

    if cpu >= 90:
        return f"Buddy, CPU usage is {cpu} percent. Your computer is working very hard."

    elif cpu >= 70:
        return f"CPU usage is {cpu} percent. A few heavy programs are running."

    else:
        return f"CPU usage is {cpu} percent."

def get_ram_usage():
    ram = psutil.virtual_memory()

    if ram.percent >= 90:
        return f"Buddy, RAM usage is {ram.percent} percent. Memory is almost full."

    elif ram.percent >= 70:
        return f"RAM usage is {ram.percent} percent."

    else:
        return f"RAM usage is {ram.percent} percent."

def get_disk_usage():
    total, used, free = shutil.disk_usage("C:\\")

    percent = round((used / total) * 100, 1)

    if percent >= 90:
        return f"Buddy, your storage is almost full. Disk usage is {percent} percent."

    else:
        return f"Disk usage is {percent} percent."