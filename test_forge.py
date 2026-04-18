#!/usr/bin/env python3
"""Quick test of upgraded forge.py features"""
import subprocess
import time

# Start forge.py with qwen2.5:0.5b model
print("Starting forge.py with qwen2.5:0.5b...")
proc = subprocess.Popen(
    ["python", "forge.py", "-m", "qwen2.5:0.5b"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

def send_command(cmd):
    """Send command to forge and wait for response."""
    proc.stdin.write(cmd + "\n")
    proc.stdin.flush()
    time.sleep(0.5)

# Test 1: /tokens command
print("\n[TEST 1] /tokens command")
send_command("/tokens")
time.sleep(1)

# Test 2: Simple task
print("\n[TEST 2] Simple task (list files)")
send_command("list files in current directory")
time.sleep(3)

# Test 3: /ctx command
print("\n[TEST 3] /ctx command")
send_command("/ctx")
time.sleep(1)

# Test 4: Exit
print("\n[TEST 4] Exit")
send_command("/exit")

print("\nTest complete!")
