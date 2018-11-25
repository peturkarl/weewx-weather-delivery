# weewx-weather-delivery
Used on raspberry PI, fetches weather data from weewx controller and sends the data to external site. 

## Setup

#### 1. Prepare environment
```sh 
# Update packages
$ sudo apt-get update

# Setup dependencies
$ sudo apt-get weewx apache2 sqlite3 python-pip git

# Setup python system packages dependencies
$ sudo apt-get install python-opencv python-picamera python3-picamera python-requests

# Setup python dependencies
$ pip install requests moment
```
#### 2. Setup project
Create and open the following file
```sh
nano /etc/weewx/skins/Standard/weewx-weather-delivery.txt.tmpl
```
Insert the following JSON to the file
```json
{
    "datetime": "$current.dateTime",
    "outTemp": "$current.outTemp",
    "windchill": "$current.windchill",
    "heatindex": "$current.heatindex",
    "dewpoint": "$current.dewpoint",
    "outHumidity": "$current.outHumidity",
    "barometer": "$current.barometer",
    "windSpeed": "$current.windSpeed",
    "windDir": "$current.windDir",
    "ordinal_compass": "$current.windDir.ordinal_compass",
    "rainRate": "$current.rainRate",
    "inTemp": "$current.inTemp",
    "UV": "$current.UV",
    "ET": "$current.ET",
    "radiation": "$current.radiation"
}
```


## Cron 

#### Change cron schedule 
```sh
# Login as user 'pi"
$ sudo crontab -e

# INSERT OR EDIT BELOW (runs every 5 minutes)
*/5 * * * * /home/pi/weewx-weather-delivery/run-script.sh
```

## Helpful commands

```sh
# Information log WEEWX
$ sudo cat /var/log/syslog | grep weewx | less

# Restart WeeWX service
$ sudo service restart weewx
```