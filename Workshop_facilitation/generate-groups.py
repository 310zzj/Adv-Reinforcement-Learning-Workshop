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
IP_DICT_J