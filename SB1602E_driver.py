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


#SB1602E general commands
Comm_SetDDRAMAddress        	= 0x80
DDRAMAddress_Ofst         		= [0x00, 0x40] 
Comm_SetCGRAM               	= 0x40
 
#SB1602E setting values
default_Contrast            	= 0x35
COMMAND                     	= 0x00
DATA                        	= 0x40
MaxCharsInALine             	= 0x10		#buffer depth for one line (no scroll function used)
NrLines							= 2

class lcd:
	
	#cursor position
	curs = [0, 0]
		
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
		"""Write one character at current position of given line"""
		if (c == '\n') or (c == '\r'):
			self.clear_rest_of_line( line )
			self.curs[line] = 0
		else:
 			self.putcxy(c, self.curs[line], line)
 			self.curs[line] += 1

	def puts(self, line, str):
		"""Write string at current position of given line"""
		for c in list(str):
			self.putc(line, ord(c))

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
