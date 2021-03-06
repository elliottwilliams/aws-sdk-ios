import re
import sys

spm_manifest_repo = '../aws-sdk-ios-spm'
version = str(sys.argv[1])

with open (f"{spm_manifest_repo}/Package.swift", 'r+') as package_manifest_file:
    content = package_manifest_file.read()
    content = re.sub('(^let latestVersion = ")([\w.]+)', r'\g<1>' + version, content, flags=re.M)
    package_manifest_file.seek(0)
    package_manifest_file.write(content)
    package_manifest_file.truncate()