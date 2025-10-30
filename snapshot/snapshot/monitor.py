import argparse
import json
import time
import os
import psutil
from datetime import datetime


class SystemMonitor:
    """Monitor system resources and output snapshots to console and file."""
    
    def __init__(self, interval=30, output_file="snapshot.json", quantity=20):
        self.interval = interval
        self.output_file = output_file
        self.quantity = quantity
        self.snapshots_taken = 0
        
    def get_snapshot(self):
        cpu_times = psutil.cpu_times_percent(interval=0.1)
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Count process states
        tasks = {"total": 0, "running": 0, "sleeping": 0, "stopped": 0, "zombie": 0}
        for proc in psutil.process_iter(['status']):
            try:
                tasks["total"] += 1
                status = proc.info['status']
                if status == psutil.STATUS_RUNNING:
                    tasks["running"] += 1
                elif status == psutil.STATUS_SLEEPING:
                    tasks["sleeping"] += 1
                elif status == psutil.STATUS_STOPPED:
                    tasks["stopped"] += 1
                elif status == psutil.STATUS_ZOMBIE:
                    tasks["zombie"] += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        snapshot = {
            "Tasks": tasks,
            "%CPU": {
                "user": round(cpu_times.user, 1),
                "system": round(cpu_times.system, 1),
                "idle": round(cpu_times.idle, 1)
            },
            "KiB Mem": {
                "total": mem.total // 1024,
                "free": mem.available // 1024,
                "used": mem.used // 1024
            },
            "KiB Swap": {
                "total": swap.total // 1024,
                "free": swap.free // 1024,
                "used": swap.used // 1024
            },
            "Timestamp": int(datetime.now().timestamp())
        }
        
        return snapshot
    
    def write_snapshot(self, snapshot):
        with open(self.output_file, "a") as file:
            json.dump(snapshot, file)
            file.write("\n")
    
    def display_snapshot(self, snapshot):
        os.system('clear')
        print(json.dumps(snapshot, indent=2), end="\r")
    
    def clear_output_file(self):
        with open(self.output_file, "w") as file:
            file.write("")
    
    def run(self):
        self.clear_output_file()
        
        while self.snapshots_taken < self.quantity:
            snapshot = self.get_snapshot()
            self.write_snapshot(snapshot)
            self.display_snapshot(snapshot)
            
            self.snapshots_taken += 1
            
            if self.snapshots_taken < self.quantity:
                time.sleep(self.interval)


def main():
    parser = argparse.ArgumentParser(description="System monitoring tool")
    parser.add_argument("-i", help="Interval between snapshots in seconds", 
                       type=int, default=30, dest="interval")
    parser.add_argument("-f", help="Output file name", 
                       default="snapshot.json", dest="output_file")
    parser.add_argument("-n", help="Quantity of snapshots to output", 
                       type=int, default=20, dest="quantity")
    
    args = parser.parse_args()
    
    monitor = SystemMonitor(
        interval=args.interval,
        output_file=args.output_file,
        quantity=args.quantity
    )
    
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")


if __name__ == "__main__":
    main()