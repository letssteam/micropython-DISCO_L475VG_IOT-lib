####################################################
###   CONSTANTES   ##############################
##############################################

LIS3MDL_FULLSCLALE_4G  = 0b00
LIS3MDL_FULLSCLALE_8G  = 0b01
LIS3MDL_FULLSCLALE_12G = 0b10
LIS3MDL_FULLSCLALE_16G = 0b11

LIS3MDL_OPERATING_MODE_LOW_POWER  = 0b00
LIS3MDL_OPERATING_MODE_MEDIUM	  = 0b01
LIS3MDL_OPERATING_MODE_HIGH 	  = 0b10
LIS3MDL_OPERATING_MODE_ULTRA_HIGH = 0b11

LIS3MDL_OUPUT_DATARATE_0_625_HZ = 0b0000
LIS3MDL_OUPUT_DATARATE_1_25_HZ  = 0b0010
LIS3MDL_OUPUT_DATARATE_2_5_HZ   = 0b0100
LIS3MDL_OUPUT_DATARATE_5_HZ     = 0b0110
LIS3MDL_OUPUT_DATARATE_10_HZ    = 0b1000
LIS3MDL_OUPUT_DATARATE_20_HZ    = 0b1010
LIS3MDL_OUPUT_DATARATE_40_HZ    = 0b1100
LIS3MDL_OUPUT_DATARATE_80_HZ    = 0b1110

LIS3MDL_MEASUREMENT_MODE_CONTINUOUS = 0b00
LIS3MDL_MEASUREMENT_MODE_SINGLE		= 0b01
LIS3MDL_MEASUREMENT_MODE_IDLE		= 0b10
LIS3MDL_MEASUREMENT_MODE_IDLE		= 0b11

LIS3MDL_OFFSET_X_REG_L = 0x05
LIS3MDL_OFFSET_X_REG_H = 0x06
LIS3MDL_OFFSET_Y_REG_L = 0x07
LIS3MDL_OFFSET_Y_REG_H = 0x08
LIS3MDL_OFFSET_Z_REG_L = 0x09
LIS3MDL_OFFSET_Z_REG_H = 0x0A
LIS3MDL_CTRL_REG1      = 0x20
LIS3MDL_CTRL_REG2      = 0x21
LIS3MDL_CTRL_REG3      = 0x22
LIS3MDL_CTRL_REG4      = 0x23
LIS3MDL_STATUS_REG     = 0x27
LIS3MDL_OUT_X_L        = 0x28
LIS3MDL_OUT_X_H        = 0x29
LIS3MDL_OUT_Y_L        = 0x2A
LIS3MDL_OUT_Y_H        = 0x2B
LIS3MDL_OUT_Z_L        = 0x2C
LIS3MDL_OUT_Z_H        = 0x2D


####################################################
###   DRIVER   ##################################
##############################################

class LIS3MDL:
	def __init__(self, i2c, address = 0x1E):
		self.i2c = i2c
		self.address = address
		self.i2c.scan()
		
		self.set_fullscale(LIS3MDL_FULLSCLALE_4G)
		self.set_operating_mode(LIS3MDL_OPERATING_MODE_HIGH)
		self.set_output_datarate(LIS3MDL_OUPUT_DATARATE_5_HZ)
		self.set_measurement_mode(LIS3MDL_MEASUREMENT_MODE_CONTINUOUS)
		
	
	def write_register(self, register, data):
		self.i2c.writeto(self.address, bytes( [register, data] ) )
	
	def read_register(self, register):
		self.i2c.writeto(self.address, bytes( [register] ) )
		return self.i2c.readfrom(self.address, 1)[0]
		
	def read_16bits_register(self, register):
		self.i2c.writeto(self.address, bytes( [register | 0x80] ) )
		return self.__to_signed( int.from_bytes( self.i2c.readfrom(self.address, 2), "little"), 16 )
		
	
	def set_fullscale(self, fs):
		self.write_register( LIS3MDL_CTRL_REG2, (fs & 0b00000011) << 5 )
		
	def set_operating_mode(self, op):
		self.write_register( LIS3MDL_CTRL_REG1, (op & 0b00000011) << 5 )
		self.write_register( LIS3MDL_CTRL_REG4, (op & 0b00000011) << 2 )
	
	def set_output_datarate(self, dr):
		self.write_register( LIS3MDL_CTRL_REG1, (dr & 0b00001111) << 1 )
	
	def set_measurement_mode(self, mm):
		self.write_register( LIS3MDL_CTRL_REG3, mm & 0b00000011 )
	
	def x(self):
		if (self.read_register(LIS3MDL_STATUS_REG) & 0b00000001) == 0:
			return None
			
		return self.read_16bits_register(LIS3MDL_OUT_X_L);
			
	def y(self):
		if (self.read_register(LIS3MDL_STATUS_REG) & 0b00000010) == 0:
			return None
			
		return self.read_16bits_register(LIS3MDL_OUT_Y_L);
	
	def z(self):
		if (self.read_register(LIS3MDL_STATUS_REG) & 0b00000100) == 0:
			return None
			
		return self.read_16bits_register(LIS3MDL_OUT_Z_L);
	
	def __to_signed(self, value, nb_bits):
		if value & (1 << (nb_bits-1) ) > 0 :
			return value - pow(2,nb_bits)
		else:
			return value

