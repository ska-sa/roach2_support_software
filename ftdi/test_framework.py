import sys, logging

import roach2_ftdi
import roach2_serial_con
#import roach2_urjtag

serial_num = "EL010001"
serial_dev = "ttyUSB2"


def menu():
   choice = 0
   while not choice == 10:
      print " ROACH2 Testing Framework"
      print " ========================"
      print " Options:"
      print " 1. FTDI EEPROM"
      print " 2. "
      print " 3. Power"
      print " 4. Setup tests"
      print " 5. PPC"
      print " 6. FPGA Built-in-tests"
      print " 7. Human Interaction Tests"
      print " 8. Run full test suit"
      print " 9. Run burn in tests (Not Implemented)"
      print " 10. quit"
      choice = input()

      if choice == 1:
         print roach2_ftdi.init_ftdi()
         print roach2_ftdi.read_serial()
         print roach2_ftdi.close_ftdi()
      elif choice == 2:
         print '2'
      elif choice == 3:
         print '3'


if __name__ == '__main__':
    from optparse import OptionParser
    
    # configure logging framework
    logger = logging.getLogger('ROACH2_tests')
    hdlr = logging.FileHandler('roach2_tests.log')
    formatter = logging.Formatter('%(levelname)s : %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

    logger.error('We have a problem')
    logger.info('We have a problem')


    p = OptionParser()
    p.add_option('-s', '--serial_number', dest='serial_num', type='str',default='XX000000',
        help='Set the serial number ie <DC010001>.')
    p.add_option('-d', '--serial_device', dest='serial_dev', type='str',default='ttyUSB2',
        help='Set the serial device to connect to ie <ttyUSB2>.')
    p.set_usage('test_framework.py <ROACH_SERIAL> [options]')
    opts, args = p.parse_args(sys.argv[1:])

    serial_num = opts.serial_num
    serial_dev = opts.serial_dev

    print serial_num
    print serial_dev

    menu()

