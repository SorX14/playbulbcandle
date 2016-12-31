# MIT License
# Copyright (c) 2016 Steve Parker

import subprocess
import shlex
from subprocess import call

class PlayBulbCandle:

	commands = {
		'setName': '0x001C', # writeReq needed get/set
		'setEffect': '0x0014', # get/set
		'setColor': '0x0016', # get/set
		'getType': '0x0023',
		'getFamily': '0x0025',
		'getFirmwareVersion': '0x0027',
		'getAppVersion': '0x0029',
		'getManufacturer': '0x002b',
		'getBatteryLevel': '0x001f',
	}

	def __init__(self, address, getName = True):
		self.address = address
		self.name = None
		if getName:
			self.getName()

	def rawComms(self, args):
		output,error = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
			
		# Retry logic
		if 'busy' in error or 'not implement' in error or 'timed out' in error:
			output,error = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
			
		ans = output.replace('Characteristic value/descriptor: ','')
		ans = ans.replace('\n','').strip()

		# Determine read or write
		commType = 'write'
		if args[3] == '--char-read':
			commType = 'read'

		# Determine address
		commAddress = args[5]

		result = {
			"device": {
				"address": self.address, 
				"name": self.name
			},
			"result": "success", 
			"msg": ans, 
			"type": commType, 
			"address": commAddress
		}

		# Remove message if its a write
		if commType == 'write':
			result['cmd'] = args[7]
		else:
			result['parsed'] = self.hexToAscii(ans)
		
		if len(error) > 0:
			result['result'] = 'error'
			result['msg'] = error
			return result

		return result

	def writeReq(self, address, value):
		try:
			cmd = 'gatttool -b ' + self.address + ' --char-write-req -a ' + address + ' -n "' + value + '"'
			args = shlex.split(cmd)
			
			return self.rawComms(args)
		except:
			pass

	def write(self, address, value):
		try:
			cmd = 'gatttool -b ' + self.address + ' --char-write -a ' + address + ' -n "' + value + '"'
			args = shlex.split(cmd)
			
			return self.rawComms(args)
		except:
			pass

	def read(self, address):
		try:
			cmd = 'gatttool -b ' + self.address + ' --char-read -a ' + address
			args = shlex.split(cmd)

			return self.rawComms(args)
		except:
			pass

	def hexToAscii(self, val):
		args = shlex.split(val)
		result = ''
		for arg in args:
			result = result + arg.decode('hex')
		return result

	def asciiToHex(self, val):
		args = list(val)
		result = ''
		for arg in args:
			result = result + arg.encode('hex')
		return result

	def constrainArg(self, val, min = 0, max = 255):
		if (val < min):
			return min
		if (val > max):
			return max
		return val

	def setName(self, value):
		self.name = value
		return self.writeReq(self.commands['setName'], self.asciiToHex(value))

	def getName(self):
		result = self.read(self.commands['setName'])
		self.name = result['parsed']
		return result

	def setEffect(self, white, red, green, blue, mode, speed):
		validModes = {'off': 'FF', 'fade': '01', 'jumpRgb': '02', 'fadeRgb': '03', 'candle': '04'}

		if mode not in validModes:
			raise AttributeError('Invalid mode')

		if mode == 'candle':
			speed = 0

		value = "%0.2X%0.2X%0.2X%0.2X%s00%0.2X00" % (self.constrainArg(white), self.constrainArg(red), self.constrainArg(green), self.constrainArg(blue), validModes[mode], self.constrainArg(speed))
		return self.write(self.commands['setEffect'], value)

	def getEffect(self):
		modes = {1: 'fade', 2: 'jumpRgb', 3: 'fadeRgb', 4: 'candle', 255: 'off'}

		result = self.read(self.commands['setEffect'])
		args = shlex.split(result['msg'])
		result['parsed'] = {
			'white': int(args[0], 16), 
			'red': int(args[1], 16), 
			'green': int(args[2], 16),
			'blue': int(args[3], 16),
			'mode': modes[int(args[4], 16)],
			'speed': int(args[6], 16)
		}
		return result

	def setColor(self, white, red, green, blue):
		value = "%0.2X%0.2X%0.2X%0.2X" % (self.constrainArg(white), self.constrainArg(red), self.constrainArg(green), self.constrainArg(blue))
		self.setEffect(0, 0, 0, 0, 'off', 0) # Sometimes blowing out the candle causes the effect to show next
		return self.write(self.commands['setColor'], value)

	def getColor(self):
		result = self.read(self.commands['setColor'])
		args = shlex.split(result['msg'])
		result['parsed'] = {
			'white': int(args[0], 16), 
			'red': int(args[1], 16), 
			'green': int(args[2], 16),
			'blue': int(args[3], 16)
		}
		return result

	def getType(self):
		return self.read(self.commands['getType'])

	def getFamily(self):
		return self.read(self.commands['getFamily'])

	def getFirmwareVersion(self):
		return self.read(self.commands['getFirmwareVersion'])

	def getAppVersion(self):
		return self.read(self.commands['getAppVersion'])

	def getManufacturer(self):
		return self.read(self.commands['getManufacturer'])

	def getBatteryLevel(self):
		result = self.read(self.commands['getBatteryLevel']);
		result['parsed'] = int(result['msg'], 16)
		return result

	def off(self):
		self.setColor(0, 0, 0, 0)