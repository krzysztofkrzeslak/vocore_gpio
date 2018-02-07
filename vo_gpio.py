import hwreg

GPIO1_MODE_REG=int("10000060",16)
GPIO2_MODE_REG=int("10000064",16)


GPIO_CTRL_BASE=int("10000600",16)
DIR_OUT=1
DIR_IN=0

GPIO_DATA_BASE=int("10000620",16)
HIGH_STATE=1
LOW_STATE=0


PermittedGpioNums={0,1,2,3,4,5,6,7,
				   8,9,10,11,12,13,14,
				   15,16,17,18,19,20,21,
				   22,23,24,25,26,27,28,29,30,
				   37,38,39,40,41,42,43,44,45,46}


setup_rules={}
#define which bits should be set/cleared in registers to initialize its gpio function

#disable uart0
setup_rules[12]= { GPIO1_MODE_REG : ( {9:0},{8:1} ) } 
setup_rules[13]= { GPIO1_MODE_REG : ( {9:0},{8:1} ) } 

#disable i2s
setup_rules[0]= { GPIO1_MODE_REG : ( {7:0}, {6:1} ) } 
setup_rules[1]= { GPIO1_MODE_REG : ( {7:0}, {6:1} ) } 
setup_rules[2]= { GPIO1_MODE_REG : ( {7:0}, {6:1} ) } 
setup_rules[3]= { GPIO1_MODE_REG : ( {7:0}, {6:1} ) } 

#disable i2c
setup_rules[5]= { GPIO1_MODE_REG : ( {21:0}, {20:1} ) } 
setup_rules[4]= { GPIO1_MODE_REG : ( {21:0}, {20:1} ) } 

#disable spi
setup_rules[6]= { GPIO1_MODE_REG : ( {12:1} ) }
setup_rules[7]= { GPIO1_MODE_REG : ( {12:1} ) }
setup_rules[8]= { GPIO1_MODE_REG : ( {12:1} ) }
setup_rules[9]= { GPIO1_MODE_REG : ( {12:1} ) }
setup_rules[10]={ GPIO1_MODE_REG : ( {12:1} ) }

#disable REFCLK
setup_rules[11]= { GPIO1_MODE_REG : ( {0:0}, {1:0} ) }

#disable UART2
setup_rules[20]= { GPIO1_MODE_REG : ( {26:1}, {27:0} ) }
setup_rules[21]= { GPIO1_MODE_REG : ( {26:1}, {27:0} ) }

#disable WDT
setup_rules[38]= { GPIO1_MODE_REG : ( {14:1} ) }

#disable REFCLK for gpio 37
setup_rules[37]= { GPIO1_MODE_REG : ( {18:1} ) }

#disable EPHY P4 LED
setup_rules[39]= { GPIO2_MODE_REG : ( {11:0} , {10:1} ) } 

#disable EPHY P3 LED
setup_rules[40]= { GPIO2_MODE_REG : ( {25:0} , {24:1}, {9:0} , {8:1} ) } 

#disable EPHY P2 LED
setup_rules[41]= { GPIO2_MODE_REG : ( {23:0} , {22:1}, {7:0} , {6:1} ) } 

#disable EPHY P1 LED
setup_rules[42]= { GPIO2_MODE_REG : ( {5:0} , {4:1} ) } 

#disable EPHY P0 LED
setup_rules[43]= { GPIO2_MODE_REG : ( {3:0} , {2:1} ) } 

#disable UART1
setup_rules[45]= { GPIO1_MODE_REG : ( {25:0} , {24:1} ) } 
setup_rules[46]= { GPIO1_MODE_REG : ( {25:0} , {24:1} ) } 
#disable SD
setup_rules[22]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
setup_rules[23]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
setup_rules[24]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
setup_rules[25]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
setup_rules[26]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
setup_rules[27]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
setup_rules[28]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
setup_rules[29]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }



def setup(gpioNum, direction):

	if gpioNum in PermittedGpioNums:
		#first set gpio mux to gpio function if needed

		if(gpioNum in setup_rules):
			for registerAddr, bitsValues in setup_rules[gpioNum].iteritems():
				for bitNumValuePair in bitsValues:
					bitNum=bitNumValuePair.keys()[0]
					bitValue=bitNumValuePair[bitNum]
					hwreg.write_bit(registerAddr,bitNum,bitValue)
					print("initialization rule for GPIO"+str(gpioNum)+",bit: "+ str(bitNum)+",value: "+str(bitValue)+" in register "+hex(registerAddr))

		#set gpio direction if gpio name is valid 
		if gpioNum in PermittedGpioNums:
			gpioCtrlReg = GPIO_CTRL_BASE + ((gpioNum/32)*4)
			bitNumber   = gpioNum % 32 if gpioNum>0 else 0

			hwreg.write_bit(gpioCtrlReg,bitNumber,direction)

			print("GPIO"+str(gpioNum)+" direction set to: "+ ("input" if direction==0 else "output") )
	else:
		print("invalid GPIO number")


def data(gpioNum, value=-1):
	if gpioNum in PermittedGpioNums:

		gpioDataReg = GPIO_DATA_BASE + ((gpioNum/32)*4)
		bitNumber   = gpioNum % 32 if gpioNum>0 else 0

		if(value != -1):
			hwreg.write_bit(gpioDataReg,bitNumber,value)
		else:
			value=hwreg.read_bit(gpioDataReg,bitNumber)

		return value

	else:
		print("invalid GPIO number")
