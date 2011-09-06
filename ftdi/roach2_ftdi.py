import ftdi, time, struct, logging

F = ftdi.ftdi_context()
E = ftdi.ftdi_eeprom()

logger = logging.getLogger("app")

# Sets up the connection to the FTDI chip
def init_ftdi(log):
   logger = log
   ftdi.ftdi_init(F)
   result = ftdi.ftdi_usb_open(F, 0x0403, 0x6011)
   if result <> 0:
      print "Unable to open ftdi device"


# Close the FTDI connection
def close_ftdi():
   ftdi.ftdi_usb_close(F)


# Write the serial number to the FTDI EEPROM
def write_serial(serial):
   if len(serial) <= 16:
      #Clear old serial
      for i in range(16):
         result = ftdi.ftdi_write_eeprom_location(F, 104+i, 0)
      # writes the length of the serial number to position 103 of the eeprom
      ftdi.ftdi_write_eeprom_location(F, 103, 768 + (len(serial) * 2 + 2))
      for i in range(len(serial)):
         char = ord(serial[i])
         result = ftdi.ftdi_write_eeprom_location(F, 104+i, char)
         if result == 0:
            print char
         else:
            print "Unable to write to ftdi eeprom"
   else:
      print "Serial must be less then 16 characters long"



# Read the serial number from the FTDI EEPROM
def read_serial():
   serial = "" 
   F.eeprom_size = 256
   result, eeprom_data = ftdi.ftdi_read_eeprom(F)
   if result == 0:
      eeprom_length = (int(hex(struct.unpack('H' * 128, eeprom_data)[103]),16)-770)/2  
      for i in range(eeprom_length):
         serial += (chr(int(hex((struct.unpack('H' * 128, eeprom_data))[104+i]),16)))
   else:
      print "Unable to read from ftdi eeprom"
   return serial


# Turns off the 
def power_force_disable():
   ftdi.ftdi_set_interface(F, ftdi.INTERFACE_D)
   ftdi.ftdi_set_bitmode(F, 0x00, ftdi.BITMODE_BITBANG) 
   ftdi.ftdi_write_data(F, '\x00', 1)


# Force power on
def power_force_on():
   ftdi.ftdi_set_interface(F, ftdi.INTERFACE_D)
   ftdi.ftdi_set_bitmode(F, 0x30, ftdi.BITMODE_BITBANG)
   ftdi.ftdi_write_data(F, '\x20', 1)


# Force power off
def power_force_off():
   ftdi.ftdi_set_interface(F, ftdi.INTERFACE_D)
   ftdi.ftdi_set_bitmode(F, 0x30, ftdi.BITMODE_BITBANG)
   ftdi.ftdi_write_data(F, '\x30', 1)


# Hold in power button for 4secs
def power_button_assert():
   ftdi.ftdi_set_interface(F, ftdi.INTERFACE_D)
   ftdi.ftdi_set_bitmode(F, 0x40, ftdi.BITMODE_BITBANG)
   ftdi.ftdi_write_data(F, '\x40', 1)
   time.sleep(4)
   ftdi.ftdi_write_data(F, '\x00', 1)


# Shortens the JTAG chain to 3 devices, PPC, FPGA, CPLD
def jtag_shorten():
   ftdi.ftdi_set_interface(F, ftdi.INTERFACE_D)
   ftdi.ftdi_set_bitmode(F, 0x08, ftdi.BITMODE_BITBANG)
   ftdi.ftdi_write_data(F, '\x08', 1)


# Expands the JTAG chain to the full 11 devices
def jtag_lengthen():
   ftdi.ftdi_set_interface(F, ftdi.INTERFACE_D)
   ftdi.ftdi_set_bitmode(F, 0x08, ftdi.BITMODE_BITBANG)
   ftdi.ftdi_write_data(F, '\x00', 1)


# Issue a halt to the PPC
def ppc_halt_on():
   ftdi.ftdi_set_interface(F, ftdi.INTERFACE_B)
   ftdi.ftdi_set_bitmode(F, 0x08, ftdi.BITMODE_BITBANG)
   ftdi.ftdi_write_data(F, '\x00', 1)


# Turn off the halt to the PPC
def ppc_halt_off():
   ftdi.ftdi_set_interface(F, ftdi.INTERFACE_B)
   ftdi.ftdi_set_bitmode(F, 0x00, ftdi.BITMODE_BITBANG)
   ftdi.ftdi_write_data(F, '\x00', 1)



#init_ftdi()
#write_serial("elpr010101")
#print read_serial()









