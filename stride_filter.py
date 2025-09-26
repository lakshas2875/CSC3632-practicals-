#!/usr/bin/env python3
import sys, os

category = input("Enter STRIDE category (e.g., Tampering): ").strip().lower()
repo = "known-cyber-attacks"

if not os.path.isdir(repo):
    print("Folder not found:", repo)
    sys.exit(1)

found = False
for root, dirs, files in os.walk(repo):
    for fname in files:
        if fname.lower().endswith(".md"):
            path = os.path.join(root, fname)
            try:
                txt = open(path, "r", encoding="utf-8", errors="ignore").read().lower()
            except:
                continue
            if category in txt:
                print(fname)            # prints file name
                found = True

if not found:
    print("No attacks matched category:", category)
