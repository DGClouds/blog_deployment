import time
import datetime
import os
import logging
import uuid
import sys

import boto3

logger = logging.getLogger("blog_backup")

TMP_BACKUP_LOCATION = "/tmp/" + str(uuid.uuid4())[:8] + ".sql"

def backup_mysql():
    os.system(f"rm {TMP_BACKUP_LOCATION}")
    os.system(f"mysqldump {os.environ.get('BACKUP_DB_NAME')} > {TMP_BACKUP_LOCATION}")

def upload_to_s3():
    tries = 1
    while True:
        try:
            s3 = boto3.client(
                's3',
                endpoint_url=os.environ.get("BACKUP_S3_ENDPOINT"),
                aws_access_key_id=os.environ.get("BACKUP_S3_KEY_ID"),
                aws_secret_access_key=os.environ.get("BACKUP_S3_ACCESS_KEY"),
            )
            s3.upload_file(
                TMP_BACKUP_LOCATION,
                os.environ.get("BACKUP_BUCKET_NAME"),
                f"{os.environ.get('BACKUP_KEY_PREFIX', '')}{datetime.datetime.now().isoformat(timespec='seconds')}.sql"
            )
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception:
            tries += 1
            if tries <= 3:
                continue
            else:
                break
        else:
            break

def clean_up():
    os.system(f"rm {TMP_BACKUP_LOCATION}")

def main():
    # main loop
    logger.debug(os.environ.items())
    pervious_exec_time: datetime.datetime = datetime.datetime(1970, 1, 1)
    while True:
        now: datetime.datetime = datetime.datetime.now()
        last_backup_duration: datetime.timedelta = now - pervious_exec_time
        if last_backup_duration >= datetime.timedelta(days=7):
            logger.info(
                f"Last backup time: {pervious_exec_time}, "
                f"exceed 7 days, execute backup process."
            )
            
            backup_mysql()
            upload_to_s3()
            clean_up()
            
            pervious_exec_time = datetime.datetime.now()
        time.sleep(3600) # 1h

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()