https://github.com/timleland/rfoutlet

https://timleland.com/wireless-power-outlets/

Copied here, just in case page goes offline:

Hardware Needed:

Etekcity 5 Pack (Try promo code: BHRMTOFF)Etekcity ZAP 5LX Auto-Programmable
433Mhz Rf Transmitter and Receiver (Backup Link)
Raspberry Pi B+ Ultimate Starter Kit
Steps:

Connect wires to Rf transmitter and receiver chips(wiring diagram). See this article for more info on gpio pins. If you would like to use different pins check out Ninjablocks 433Utils   GPIO Pin Layout
Install Rasbian on Raspberry Pi (If using Raspbian Jessie use /var/www/html/rfoutlet for all paths below)
Install Wiring Pi
Install Apache and PHP on the Raspberry Pi
Clone web files
Make sure you have git installed. If not, type: sudo apt-get install git
Type: sudo git clone https://github.com/timleland/rfoutlet.git /var/www/rfoutlet
Use RFSniffer to find RF codes for your devices
Type: sudo /var/www/rfoutlet/RFSniffer
Record all 6 digit codes for on/off for each outlet
Update toggle.php with your codes and pulse
Type: sudo nano /var/www/rfoutlet/toggle.php
If the Received pulse is different than 189, you should edit line 38 to your pulse length
Edit lines 6-27 wth your codes
If you’re using a different pin than 0, Edit line 35
Use ctrl + x then “y” to save your file
Change permission of codesend program so sudo isn’t required:
Type: sudo chown root.root /var/www/rfoutlet/codesend
Type: sudo chmod 4755 /var/www/rfoutlet/codesend
You should now be able to turn the outlets on/off from the command line.
Type: ./codesend 349491 -l 198 -p 0
-l is for pulse length and -p is for different pins
Browse to Raspberry Pi ip address ‘http://<your-pi-ip>/rfoutlet/ App demo
Now you should be able to power on/off your outlets from a web browser. If you would like more range you can add an antenna to the transmitter chip. I cut a 12 inch wire from a cat 5 cable and it worked great.
If you would like to schedule the outlets on or off you could use crontab. Here is an example to run everyday at 8pm.
00 20 * * * /var/www/rfoutlet/codesend “code number”
