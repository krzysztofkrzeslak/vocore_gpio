# vocore_gpio
this is a simple python module for driving vocore2 gpio

# usage
Usage is very simple, package provide 2 methods		
`setup(gpioNumber, direction)` - setup gpio as output(1) or input(0) )		
	
	
`data(gpioNumber, value[optional] )` - set or reads gpio data, if gpio is set as output value specify state(1-HIGH, 0-LOW), if gpio is set as input method returns gpio value		

in file led_blink.py is script which should blink onboard led if everything is working fine



