#!/bin/bash
#
# weewx_backup_to_ftp.sh
# Script for backing up sqlite3 database
# Intended for use with cron for regular automated backups
#

# Configurations
DB="/var/lib/weewx/weewx.sdb"
LOG="/home/pi/weewx-weather-delivery/logs/backup.log"
OUTPUT_FILENAME_BASE="weewx_backup_db_"
FTP_SERVER_DIRECTORY="backups_pi_arnavollur"

# Environment variables
HOST="example.host.com"
USER="ftp_username"
PASS="ftp_password"

DATE=`date '+%Y-%m-%d-%H:%M'`

# check to see if $DB exists
if [ ! -f $DB ]
then
    echo $(date +"%Y-%m-%d %T") -- cannot find the database at the following path: $DB >> $LOG
    exit 1
fi

# Check if environment variables are set for connecting to external FTP
if [ -z "$HOST" ] || [ -z "$USER" ] || [ -z "$PASS" ];
then
    echo "No connection variables found, please set correct variables?"
    exit 1
fi

# Export to external FTP
if nc -z -w1 "$HOST" 21; then
    # Access available: Upload to server
    curl -T "$DB" ftp://$USER:$PASS@$HOST/$FTP_SERVER_DIRECTORY/backup-$(date +%F_%H-%M-%S).db

    # DONE
else
    echo "FTP is down. Will not upload backup file.. exiting."
    exit 1
fi