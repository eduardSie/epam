"""
Make snapshot

{"Tasks": {"total": 440, "running": 1, "sleeping": 354, "stopped": 1, "zombie": 0},
"%CPU": {"user": 14.4, "system": 2.2, "idle": 82.7},
"KiB Mem": {"total": 16280636, "free": 335140, "used": 11621308},
"KiB Swap": {"total": 16280636, "free": 335140, "used": 11621308},
"Timestamp": 1624400255}
"""
import argparse
import psutil
import time
import json
import os


class SystemMonitor:

    def get_snapshot(self):

        tasks_data = {
            "total": 0,
            "running": 0,
            "sleeping": 0,
            "stopped": 0,
            "zombie": 0
        }
        for proc in psutil.process_iter(['status']):
            tasks_data['total'] += 1
            try:
                status = proc.info['status']
                if status == psutil.STATUS_RUNNING:
                    tasks_data['running'] += 1
                elif status == psutil.STATUS_SLEEPING:
                    tasks_data['sleeping'] += 1
                elif status == psutil.STATUS_STOPPED:
                    tasks_data['stopped'] += 1
                elif status == psutil.STATUS_ZOMBIE:
                    tasks_data['zombie'] += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        cpu_stats = psutil.cpu_times_percent()
        cpu_data = {
            "user": cpu_stats.user,
            "system": cpu_stats.system,
            "idle": cpu_stats.idle
        }

        mem = psutil.virtual_memory()
        mem_data = {
            "total": mem.total // 1024,
            "free": mem.free // 1024,
            "used": mem.used // 1024
        }

        swap = psutil.swap_memory()
        swap_data = {
            "total": swap.total // 1024,
            "free": swap.free // 1024,
            "used": swap.used // 1024
        }

        timestamp = int(time.time())

        snapshot = {
            "Tasks": tasks_data,
            "%CPU": cpu_data,
            "KiB Mem": mem_data,
            "KiB Swap": swap_data,
            "Timestamp": timestamp
        }
        return snapshot


def main():
    parser = argparse.ArgumentParser(description="System monitoring snapshot tool.")

    parser.add_argument("-i", help="Interval between snapshots in seconds", type=int, default=30)
    parser.add_argument("-f", help="Output file name", default="snapshot.json")
    parser.add_argument("-n", help="Quantity of snapshot to output", type=int, default=20)
    args = parser.parse_args()

    monitor = SystemMonitor()

    open(args.f, "w").close()

    for i in range(args.n):
        snapshot_data = monitor.get_snapshot()

        os.system('clear')
        print(f"Snapshot {i + 1}/{args.n} (Interval: {args.i}s)")
        print(json.dumps(snapshot_data, indent=4))

        with open(args.f, "a") as file:
            json.dump(snapshot_data, file)
            file.write("\n")

        if i < args.n - 1:
            time.sleep(args.i)


