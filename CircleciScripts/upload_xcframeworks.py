import boto3
from botocore.exceptions import ClientError
from framework_list import xcframeworks
from functions import log, run_command

def upload_file(file_name, bucket, object_name): 
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
        
project_dir = os.getcwd()
archive_path = f"{project_dir}/xcframeworks/output/archives"

accessToken = sys.argv[1]
idToken = sys.argv[2]
sessionToken = sys.argv[3]

log(f"Uploading xcframeworks from {archive_path}")
for framework in xcframeworks:
    filename = f"{framework}.xcframework.zip"
    archived_sdk_path = f"{archive_path}/{filename}"
    upload_file(archived_sdk_path, "", filename)