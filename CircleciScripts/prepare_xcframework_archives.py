import os
import sys
import shutil
import re

from framework_list import xcframeworks
from functions import log, run_command

def create_archives(xcframework_path, archive_path):
    for framework in xcframeworks:
        log(f"Creating zip file for {framework}")
        xcframework_sdk_path = f"{xcframework_path}/{framework}.xcframework"
        archived_sdk_path = f"{archive_path}/{framework}.xcframework"
        shutil.make_archive(archived_sdk_path, 'zip', xcframework_sdk_path)

def create_checksum(archive_path, spm_manifest_repo):
    framework_to_checksum = {}
    for framework in xcframeworks:
        zipfile_path = f"{archive_path}/{framework}.xcframework.zip"
        cmd = [
            "swift",
            "package",
            "--package-path",
            spm_manifest_repo,
            "compute-checksum",
            zipfile_path
        ] 
        
        (exit_code, out, err) = run_command(cmd, keepalive_interval=300, timeout=7200)
        if exit_code == 0:
            log(f"Created check sum for archive {framework} {out}")
        else:
            log(cmd)
            log(f"Could not create checksum for archive: {framework} output: {out}; error: {err}")
            sys.exit(exit_code)
        framework_to_checksum[framework] = out.decode("utf-8").rstrip()
    return framework_to_checksum

def update_spm_manifest(framework_to_checksum, spm_manifest_repo):
    with open (f"{spm_manifest_repo}/Package.swift", 'r+') as package_manifest_file:
        content = package_manifest_file.read()
        for framework in xcframeworks:  
            checksum = framework_to_checksum[framework]
            content = re.sub('(^ +"'+framework+'"\: ")([\w.]+)', r'\g<1>' + checksum, content, flags=re.M)
        package_manifest_file.seek(0)
        package_manifest_file.write(content)
        package_manifest_file.truncate()

project_dir = os.getcwd()
xcframework_path = f"{project_dir}/xcframeworks/output/XCF"
archive_path = f"{project_dir}/xcframeworks/output/archives"
spm_manifest_repo = '../aws-sdk-ios-spm'

log(f"Creating archives from {xcframework_path}")
create_archives(xcframework_path, archive_path)

log(f"Calculating checksum from {archive_path}")
framework_to_checksum = create_checksum(archive_path, spm_manifest_repo)

log(f"Updating checksum to {spm_manifest_repo}")
update_spm_manifest(framework_to_checksum, spm_manifest_repo)