import os

files_to_check = [
    'tp(9).py',
    'main.py', 
    'buildozer.spec',
    'setup.py',
    'icon.png'
]

print("=== 文件检查 ===")
for f in files_to_check:
    exists = os.path.exists(f)
    size = os.path.getsize(f) if exists else 0
    print(f"{f}: {'存在' if exists else '不存在'} ({size} bytes)")