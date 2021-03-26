"""import boto3


s3_ = boto3.client("s3") 
objects = s3_.list_objects(Bucket="lbst2020-student-avneet")
print(len(objects))

for object_ in objects['Contents']:
	keys.append(object_['Key'])"""

import boto3
import os

s3 = boto3.resource('s3') # assumes credentials & configuration are handled outside python in .aws directory or environment variables

def download_s3_folder(bucket_name, s3_folder, local_dir=None):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_folder):
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':
            continue
        bucket.download_file(obj.key, target)


download_s3_folder('lbst2020-student-avneet', 'parcels', local_dir="D:/DHI/DataUpdated/Parcels")