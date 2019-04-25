# weewx-weather-delivery
Used on raspberry PI, fetches weather data from weewx controller and sends the data to external site. 

## Setup

### 1. Prepare environment
```sh 
# Update packages
$ sudo apt-get update

# Setup dependencies
$ sudo apt-get install sqlite3 python-pip git

# Setup WeeWx
[Instructions](http://www.weewx.com/docs/debian.htm)

# Setup python system packages dependencies
$ sudo apt-get install python-opencv python-picamera python3-picamera python-requests

# Setup python dependencies
$ sudo pip install requests moment
```
### 2. Setup weewx run scripts
This method uses the skin engine for weewx to generate a JSON output to file, which our script can read from. This saves the trouble of accessing the database. You'll need to create a template and add that template to the skin config. 

Create and open the following file
```sh
sudo nano /etc/weewx/skins/Standard/weewx-weather-delivery.txt.tmpl
```
Insert the following JSON to the file
```json
{
    "datetime": "$current.dateTime.format('%d-%b-%Y %H:%M')",
    "outTemp": "$current.outTemp",
    "inTemp": "$current.inTemp",
    "heatindex": "$current.heatindex",
    "outHumidity": "$current.outHumidity",
    "barometer": "$current.barometer",
    "windchill": "$current.windchill",
    "windSpeed": "$current.windSpeed",
    "windDir": "$current.windDir",
    "windGust": "$current.windGust",
    "ordinal_compass": "$current.windDir.ordinal_compass",
    "dewpoint": "$current.dewpoint",
    "rainRate": "$current.rainRate",
    "UV": "$current.UV",
    "ET": "$current.ET",
    "radiation": "$current.radiation"
}
```
Activate the Report feature, open the config file for weewx
```sh 
$ nano /etc/weewx/weewx.conf
``` 
Change the following code under the "**[[StandardReport]]**" code block (*around line 192*)
```
        enable = true
```

Edit this file
```sh 
$ nano /etc/weewx/skins/Standard/skin.conf
``` 
Add the following code to the "**[CheetahGenerator]**" code block (*around line 200*)

**Reminder**: Save file after adding the code
```
[[weewx-weather-delivery]]
        encoding = strict_ascii
        template = weewx-weather-delivery.txt.tmpl
```

Restart service and make sure it starts up correctly
```sh
$ sudo service weewx restart
```

### 3. Fetch the project files and configure
```sh
$ cd /home/pi
$ git clone https://github.com/peturkarl/weewx-weather-delivery.git

# Set cron script to executable
$ cd weewx-weather-delivery
$ sudo chmod +x run-script.sh
$ sudo chmod 744 run-script.sh
$ touch logs/cron-delivery.log
$ sudo chmod 777 logs/cron-delivery.log
```

### 4. Setup cron schedules
```sh
# Login as user 'pi"
$ sudo crontab -e

# Run image upload (runs every 5 minutes)
*/5 * * * * /home/pi/weewx-weather-delivery/run-script.sh >/home/pi/weewx-weather-delivery/logs/cron-delivery.log 2>&1 

# Restart WeeWX every morning at 08:00
0 8 * * * /etc/init.d/weewx restart

```

### 5. Setup backups to external FTP
```sh
# -------------------------------
# Make sure you add your OWN credentials to this file (/home/pi/weewx-weather-delivery/weewx_backup_to_ftp.sh)
#--------------------------------

# Set the backup script as executable
$ sudo chmod +x /home/pi/weewx-weather-delivery/weewx_backup_to_ftp.sh

# Runs every sunday at midnight, sends DB backup to FTP server
0 0 * * 0 /home/pi/weewx-weather-delivery/weewx_backup_to_ftp.sh >/home/pi/weewx-weather-delivery/logs/cron-delivery.log 2>&1 
```



## Helpful commands
```sh
# Information log WEEWX
$ sudo cat /var/log/syslog | grep weewx | less

# Restart WeeWX service
$ sudo service restart weewx

# Update code from Git repository (you might have some issues with file permissions)
$ git pull origin master

# Fetch latest cron log entries(if job successfully run then it's written to the log, else the error is printed)
$ tail -n 15 /home/pi/weewx-weather-delivery/logs/cron-delivery.log

# Find out which USB bus is active
$ ls /dev/ttyUSB*

```
