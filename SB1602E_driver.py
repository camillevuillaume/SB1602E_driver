"""
This is a Python driver for I2C text LCD with a command set compatible with the SB1602E.
It was tested with the following 8x2 LCD from switch-science:
http://www.switch-science.com/catalog/1516/

The software is based on the SB1602E C library by Ted Okano.
http://mbed.org/users/okano/code/TextLCD_SB1602E/file/694061176edf/TextLCD_SB1602E.h

Copyright (c) 2014 Camille Vuillaume
Released under the MIT License
"""

import smbus
from time import *

ADDRESS 						= 0x3E

#original datasheet
Comm_FunctionSet_Normal			= 0x38
Comm_FunctionSet_Extended		= 0x39
Comm_InternalOscFrequency		= 0x14
Comm_ContrastSet				= 0x70
Comm_PwrIconContrast			= 0x5C
Comm_FollowerCtrl				= 0x60
Comm_DisplayOnOff				= 0x0C
Comm_ClearDisplay				= 0x01
Comm_EntryModeSet				= 0x04
Comm_ReturnHome					= 0x02

Comm_SetDDRAMAddress			= 0x80
DDRAMAddress_Ofst				= [0x00, 0x40]

#SB1602E setting values
default_Contrast            	= 0x35
COMMAND                     	= 0x00
DATA                        	= 0x40

#Model-dependent
MaxCharsInALine             	= 0x08
NrLines							= 2

class lcd:
	
	#cursor position
	curs = [0, 0]
	string = ["", ""]
		
	def __init__(self):
		"""LCD initialization"""
		self.bus = smbus.SMBus(1)
		#initialize LCD
		sleep(0.04)
		self.lcd_command(Comm_FunctionSet_Normal)		
		sleep(30e-6)
		self.lcd_command(Comm_ReturnHome)
		sleep(30e-6)
		self.lcd_command(Comm_FunctionSet_Extended)
		sleep(30e-6)
		self.lcd_command(Comm_InternalOscFrequency)
		sleep(30e-6)
		self.lcd_command(Comm_ContrastSet | ( default_Contrast & 0xF))
		sleep(30e-6)
		self.lcd_command(Comm_PwrIconContrast | ((default_Contrast >> 4) & 0x3))
		sleep(30e-6)
		self.lcd_command(Comm_FollowerCtrl | 0x0A)
		sleep(0.2)
		self.lcd_command(Comm_DisplayOnOff)
		sleep(30e-6)
		self.lcd_command(Comm_ClearDisplay)
		sleep(30e-6)
		self.lcd_command(Comm_EntryModeSet)
		sleep(0.0011)
	
	def clear_rest_of_line(line):
		"""Clear remaining part of line"""
		for i in range(curs[line], MaxCharsInALine):
			self.putcxy(' ', i, line)

	def clear(self):
		"""clear the LCD"""	
		self.lcd_command( Comm_ClearDisplay );
		sleep(2e-3);
		self.curs[0]    = 0
		self.curs[1]    = 0
		
	def putcxy(self, c, x, y):
		"""Write character at position x y"""
		if (x < MaxCharsInALine) and (y < NrLines):
			self.lcd_command( (Comm_SetDDRAMAddress | DDRAMAddress_Ofst[ y ]) + x)
			self.lcd_data(c)

	def putc(self, line, c):
		"""Write one character at current position of given line
		Returns the number of characters left in given line
		"""
		if (c == '\n') or (c == '\r'):
			self.clear_rest_of_line( line )
			self.curs[line] = MaxCharsInALine
			return 0
		elif self.curs[line] < MaxCharsInALine:
 			self.putcxy(c, self.curs[line], line)
 			self.curs[line] += 1
 		return MaxCharsInALine - self.curs[line]

	def puts(self, line, str):
		"""Write string at current position of given line
		Returns the number of characters left in given line
		"""
		CharsLeft = 0
		for c in list(str):
			CharsLeft =  self.putc(line, ord(c))
			if CharsLeft <= 0:
				break
		return CharsLeft
		
	def puts(self, str):
		"""Clear LCD and write string"""
		self.clear()
		line = 0
		for c in list(str):
			CharsLeft =  self.putc(line, ord(c))
			if CharsLeft <= 0:
				line += 1
				if line >= NrLines:
					break
	
	def puts_scroll(self, str1, str2):
		"""Endlessly scroll strings from left to right and then right to left"""
		i = 0
		j = 0
		incr_i = 1
		incr_j = 1
		while 1:
			self.clear()
			for c in list(str1)[i: i+MaxCharsInALine]:
				self.putc(0, ord(c))
			for c in list(str2)[j: j+MaxCharsInALine]:
				self.putc(1, ord(c))
			i += incr_i
			j += incr_j
			if i == 0 and j == 0:
				incr_i = 1
				incr_j = 1
				sleep(0.5)
			elif i+MaxCharsInALine == len(str1) and j+MaxCharsInALine == len(str2):
				incr_i = -1
				incr_j = -1	
				sleep(0.5)			
			elif i == 0 or i+MaxCharsInALine == len(str1):
				incr_i = 0
			elif j == 0 or j+MaxCharsInALine == len(str2):
				incr_j = 0
			sleep(0.5)
			
	def set_contrast(constrast):
		"""Set LCD contrast"""
		self.lcd_command(Comm_FunctionSet_Extended )
		self.lcd_command(Comm_ContrastSet |  (contrast     & 0x0f))
		self.lcd_command(Comm_PwrIconContrast | ((contrast>>4) & 0x03))
		self.lcd_command(Comm_FunctionSet_Normal)	
			
	def lcd_command(self, command):
		"""Low level function to send command"""
		self.bus.write_byte_data(ADDRESS, COMMAND, command)
		sleep(0.0001)
		
	def lcd_data(self, data):
		"""Low level function to send data"""
		self.bus.write_byte_data(ADDRESS, DATA, data)
		sleep(0.0001)
