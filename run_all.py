#!/usr/bin/env python3
"""
Run both AquaVaults servers (bridge.py and serve.py) in parallel.
Press Ctrl-C to stop them cleanly.
"""

import subprocess
import time
import signal
import sys

procs = [
    {"name": "Click Confirm (Flask)", "cmd": ["python", "click_confirm.py"], "proc": None},
    {"name": "Swapper Static Server", "cmd": ["python", "serve.py"], "proc": None},
]

def start_all():
    for entry in procs:
        print(f"🚀 Starting {entry['name']} ...")
        entry["proc"] = subprocess.Popen(entry["cmd"])
        time.sleep(1.5)  # brief stagger to avoid port-race
    print("✅ Both servers running. Press Ctrl-C to stop.")

def stop_all():
    print("\n🛑 Stopping all processes...")
    for entry in procs:
        p = entry["proc"]
        if p and p.poll() is None:
            print(f"  • Terminating {entry['name']} (pid {p.pid})")
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"  ⚠️  {entry['name']} didn’t exit in 5 s → killing")
                p.kill()
    print("✅ All processes stopped cleanly.\n")

def monitor():
    while True:
        time.sleep(3)
        for entry in procs:
            p = entry["proc"]
            if p and p.poll() is not None:
                code = p.returncode
                print(f"❌ {entry['name']} exited unexpectedly (code {code})")
                stop_all()
                sys.exit(1)


if __name__ == "__main__":
    try:
        start_all()
        monitor()   # loop until crash or Ctrl-C
    except KeyboardInterrupt:
        stop_all()
        sys.exit(0)
