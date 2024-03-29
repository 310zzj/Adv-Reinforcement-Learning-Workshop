import logging
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
import os
import json
import argparse
import shutil
import pandas as pd

TMP_FOLDER = 'LINK_TEMP'
IP_DICT_JSON_NAME = 'active_ips.json'
GROUP_DICT_NAME = 'groups.json'
GROUP_EXCEL_NAME = 'Groups.xlsx'
AMI_ID = 'ami-060e29600c7769bc0'


def bucket_exists(bucket_name):
    """Determine whether bucket_name exists and the user has permission to access it

    :param bucket_name: string
    :return: True if the referenced bucket_name exists, otherwise False
    """

    s3 = boto3.client('s3')
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.debug(e)
        return False
    return True


def write_json(d, dest):
    with open(dest, 'w') as cred:
        json.dump(d, cred)


def load_json(dest):
    with open(dest, 'r') as cred:
        return json.load(cred)


def list_ec2():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()

    running_ws_ips = {}

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            if instance['ImageId'] == AMI_ID \
                    and instance['State']['Name'] == 'running':

                running_ws_ips[instance['InstanceId']] = \
                    instance['NetworkInterfaces'][0]['Association']['PublicIp']

    print(f'\nFound the running ec2 instances:')
    print(f'{running_ws_ips}\n')

    return running_ws_ips


def download_files(bucket_name, LINK_FOLDER):

    ip_dict = list_ec2()

    if Path(TMP_FOLDER).exists():
        shutil.rmtree(TMP_FOLDER)
    os.mkdir(TMP_FOLDER)


    s3 = boto3.resource('s3')
    rl_bucket = s3.Bucket(bucket_name)

    # Downloads only files with an ip as name in the bucket
    for element in rl_bucket.objects.all():

        element_list = element.key.split('/')

        if element_list[0] == LINK_FOLDER and os.path.splitext(
                element_list[-1])[-1] == '.txt':
            p_ip, _ = os.path.splitext(element_list[-1])

            if p_ip in ip_dict.values():

                s3.meta.client.download_file(bucket_name,
                                             element.key,
                                             str(Path(TMP_FOLDER).joinpath(
                                                 element_list[-1])))

    # Save the ip dict to track last active ec2 instances
    write_json(ip_dict, IP_DICT_JSON_NAME)


def allocate_new_groups():

    ip_active_dict = load_json(IP_DICT_JSON_NAME)

    if Path(GROUP_DICT_NAME).exists():
        os.remove(Path(GROUP_DICT_NAME))

    group_dict = {}

    group_num