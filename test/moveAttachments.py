"""
导出程序默认放到
"""
import os

folders =[]

for root, dirs, _ in os.walk("D:\\markdown_note"):
    for dir in dirs:
        if dir.endswith(".assets") :
            folders.append((root, dir))


for (root, dir) in folders:
    org = os.path.join(root, dir)
    target = os.path.join(root, '.assets\\' + dir.replace('.assets', ''))
    print(org, target)

    os.path.join(root, '.assets')
    os.makedirs(root + '\\.assets', exist_ok=True)
    os.rename(org, target)
