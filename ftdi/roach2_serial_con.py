import serial

class r2_serial_conn:

   serial_num = 'TE010001'
   
   def __init__(self):
      self.ser = serial.Serial('/dev/ttyUSB2', 115200, bytesize=8 ,parity=serial.PARITY_NONE, stopbits=1, timeout=1)
      self.log_file = open("r2_test.log", 'w')
      if self.ser.isOpen():
         self.log_file.write("Serial connection initialised")
      return self.ser.isOpen()
   
   
   def close_serial(self):
      ser.close()
      if not ser.isOpen():
         log_file.write("Serial connection close")
      return not ser.isOpen()
   
   
   def sensor(self):
      if self.ser.isOpen():
         self.ser.write('r2sensor\r')
         self.log_file.write(ser.readall())
   
   
   def power_down(self):
      if ser.isOpen():
         ser.write('r2gpio set killn 0\r')
         log_file.write(ser.readall())
   
   
   def rtc(self):
      if ser.isOpen():
         ser.write('r2rtc\r')
         log_file.write(ser.readall())
         output = ser.readall()
   
   
   def set_mac(self):
      if ser.isOpen():
         ser.write('setenv 02:34:35:01:00:01\r')
         ser.write('saveenv\r')
         ser.write('printenv\r')
         log_file.write(ser.readall())
   
   
   def idle_errors(self):
      if ser.isOpen():
         ser.write('mii read 1 a\r')
         log_file.write(ser.readall())
         ser.write('mii read 7 a\r')
         log_file.write(ser.readall())
   
   
   def usb_check(self):
      if ser.isOpen():
         ser.write('usb info\r')
         log_file.write(ser.readall())
         ser.write('usb start')
         log_file.write(ser.readall())
   
   
   def rev_num(self):
      if ser.isOpen():
         ser.write('md.b c0000000\r')
         log_file.write(ser.readall())
   

