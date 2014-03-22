SB1602E_driver
==============

Python driver for SB1602E I2C LCD

This is a Python driver for I2C text LCD with a command set compatible with the SB1602E.
It was tested with the following 8x2 LCD from switch-science:
http://www.switch-science.com/catalog/1516/
The LCD itself comes from Akizuki Denshi, product reference AQM0802A-RN-GBW.
http://akizukidenshi.com/catalog/g/gP-06669/

The following instructions must be followed in order to use I2C from Python on the Raspberry Pi.
- In /etc/modprobe.d/raspi-blacklist.conf, comment out (with sudo nano) the following line: blacklist i2c-bcm2708
- Add the following line (with sudo nano) to /etc/modules: i2c-dev
- Install i2c-tools and python-smbus with sudo apt-get install
- Add the pi to the i2c group with sudo adduser pi i2c
- Reboot with sudo reboot
- Check the address of the LCD with i2cdetect -y 1 (was 0x3e for me) and if necessary, modify it in SB1602E_driver.py

