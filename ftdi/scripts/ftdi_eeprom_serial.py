import ftdi
import time
import struct

F = ftdi.ftdi_context()
E = ftdi.ftdi_eeprom()


def init_ftdi():
   ftdi.ftdi_init(F)
   result = ftdi.ftdi_usb_open(F, 0x0403, 0x6011)
   if result <> 0:
      print "Unable to open ftdi device"


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

def read_serial():
   serial = "" 
   F.eeprom_size = 256
   result, eeprom_data = ftdi.ftdi_read_eeprom(F, "256")
   if result == 0:
      eeprom_length = (int(hex(struct.unpack('H' * 128, eeprom_data)[103]),16)-770)/2  
      for i in range(eeprom_length):
         serial += (chr(int(hex((struct.unpack('H' * 128, eeprom_data))[104+i]),16)))
   else:
      print "Unable to read from ftdi eeprom"
   return serial



#init_ftdi()
#write_serial("elpr010101")
#print read_serial()
