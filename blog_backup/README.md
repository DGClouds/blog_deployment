# dgideas.net blog backup service
This backup service automatically backup necessary files on:
* after every reboot, and
* 7 days(or other duration) after pervious successful backup
## Requirements
* Python3
* venv with requirement.txt installed
## Install
1. clone the whole repo to `~`, and move the directory into `/opt`(need sudo right)

2. change environment variables on blog_backup.service:

| env | description | example |
| --- | --- | --- |
| `BACKUP_S3_ENDPOINT` | S3 compatible service endpoint | |
| `BACKUP_S3_KEY_ID` | api key id | |
| `BACKUP_S3_ACCESS_KEY` | api access key | |
| `BACKUP_BUCKET_NAME` | bucket name where backup file stored | |
| `BACKUP_KEY_PREFIX` | backup filename prefix, the format is `{prefix}{iso format datetime}`, default `""` | |
| `BACKUP_DB_NAME` | Wordpress mysql db name, default `wordpress` | |

changes these settings on blog_backup.service if necessary:
* User=root

3. create `~/.my.cnf` file with the following contents:
```
[mysqldump]
user=your_mysql_username
password=your_mysql_password
```

4. `cd /opt/blog_deployment/blog_backup`
5. `python3 -m venv venv`
6. `source /opt/blog_deployment/blog_backup/venv/bin/activate`
7. `pip3 install -r requirement.txt`
8. `cp blog_backup.service /lib/systemd/system/`
9. `systemctl enable blog_backup.service`
10. run this service now and check running status: `systemctl start blog_backup && systemctl status blog_backup.service`

## unittest
`python3 -m unittest discover`
