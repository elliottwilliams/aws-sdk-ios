import os
import sys
import shutil

from framework_list import xcframeworks
from functions import log, run_command

project_dir = os.getcwd()
xcframework_path = f"{project_dir}/xcframeworks/output/XCF/"

log(f"Uploading xcframeworks from {xcframework_path}")

for framework in xcframeworks:
    
    log(f"Creating zip file for {framework}")
    zipfile_name = f"{framework}.xcframework"
    zipfile_path = f"{xcframework_path}{framework}.xcframework.zip"
    shutil.make_archive(f"{xcframework_path}/{zipfile_name}", 'zip', f"{xcframework_path}/{framework}.xcframework")
    
    log(f"Uploading {zipfile_path} to S3")

    log(f"Store checksum")
    #swift package compute-checksum path/to/MyFramework.zip
    cmd = [
        "swift",
        "package",
        "--package-path",
        "../aws-sdk-ios-spm",
        "compute-checksum",
        zipfile_path
    ] 
    
    (exit_code, out, err) = run_command(cmd, keepalive_interval=300, timeout=7200)
    if exit_code == 0:
        log(f"Created check sum for archive {out}")
    else:
        log(cmd)
        log(f"Could not create checksum for archive: {framework} output: {out}; error: {err}")
        sys.exit(exit_code)
