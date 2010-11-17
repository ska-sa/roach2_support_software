from jtag_decode import *
from Open_Array import *
from auto_generate_c import *

#main
if __name__ == '__main__':

  input_file_1 = 'msr.csv'
  input_file_2 = 'pc.csv'
  input_file_3 = 'word.csv'
  input_file_4 = 'wtlb0.csv'

  filename = 'auto_demo.c'
  f = open(filename, 'wb')
  
  generate_header(f) #generate c-headers

  generate_prototype('int','msr','int',f)
  generate_prototype('int','pc','int',f)
  generate_prototype('int','word','int',f)
  generate_prototype('int','wtlb','int',f)
  generate_prototype('int','ftdi','void',f)
  f.write('\n') #seperate prototypes from main

  generate_main(f)  #generate 'main' function in C
  f.write('\n') #place empty line in main
  close_main(f)     #close 'main' function
  f.write('\n') #seperate main from functions

  generate_func('int','ftdi','void',f) #generate ftdi setup function
  print 'Generating ftdi function.'
  ftdi_setup(f)     #c-code to setup ftdi chip
  reset_chain(f)    #reset jtag to 
  jtag_setup(f)     #setup ftdi jtag settings
  run_test_idle(f)  #goto run test idle state
  close_func(f)

  generate_func('int','msr','int',f)
  print 'Generating msr function.'
  data_dictionary = open_file_to_array(input_file_1)
  jtag_decode(data_dictionary, f) #interpret csv file to jtag commands
  #f.write('return xxx')
  close_func(f)

  generate_func('int','pc','int',f)
  print 'Generating pc function'
  data_dictionary = open_file_to_array(input_file_2)
  jtag_decode(data_dictionary, f) #interpret csv file to jtag commands
  close_func(f)

  generate_func('int','word','int',f)
  print 'Generating word function'
  data_dictionary = open_file_to_array(input_file_3)
  jtag_decode(data_dictionary, f) #interpret csv file to jtag commands
  close_func(f)

  generate_func('int','wtlb','int',f)
  print 'Generate wtlb function.'
  data_dictionary = open_file_to_array(input_file_4)
  jtag_decode(data_dictionary, f) #interpret csv file to jtag commands
  close_func(f)

  ftdi_close(f)     #close ftdi chip
  f.close()         #close file
  
