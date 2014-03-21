"""
Test for the SB1602 Python driver

Copyright (c) 2014 Camille Vuillaume
Released under the MIT License
"""

import SB1602E_driver
from time import *

#LCD initialization
lcd = SB1602E_driver.lcd()

#LCD clear
lcd.clear()

#Hello world
lcd.puts_scroll("Hello World !", "World Hello")

#lcd.puts(0, "Hello")
#lcd.puts(1, "World !")

