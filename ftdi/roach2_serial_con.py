import serial

serial_num = 'TE010001'

ser = ''
log_file = open("r2_test.log", 'w')

def init():
   ser = serial.Serial('/dev/ttyUSB2', 115200, bytesize=8 ,parity=serial.PARITY_NONE, stopbits=1, timeout=1)
   if ser.isOpen():
      log_file.write("Serial connection initialised")
   return ser.isOpen()


def close_serial():
   ser.close()
   if not ser.isOpen():
      log_file.write("Serial connection close")
   return not ser.isOpen()


def sensor():
   if ser.isOpen():
      ser.write('r2sensor\r')
      log_file.write(ser.readall())


def power_down():
   if ser.isOpen():
      ser.write('r2gpio set killn 0\r')
      log_file.write(ser.readall())


def rtc():
   if ser.isOpen():
      ser.write('r2rtc\r')
      log_file.write(ser.readall())
      output = ser.readall()


def set_mac():
   if ser.isOpen():
      ser.write('setenv 02:34:35:01:00:01\r')
      ser.write('saveenv\r')
      ser.write('printenv\r')
      log_file.write(ser.readall())


def idle_errors():
   if ser.isOpen():
      ser.write('mii read 1 a\r')
      log_file.write(ser.readall())
      ser.write('mii read 7 a\r')
      log_file.write(ser.readall())


def usb_check():
   if ser.isOpen():
      ser.write('usb info\r')
      log_file.write(ser.readall())
      ser.write('usb start')
      log_file.write(ser.readall())


def rev_num():
   if ser.isOpen():
      ser.write('md.b c0000000\r')
      log_file.write(ser.readall())


