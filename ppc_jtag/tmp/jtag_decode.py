#!/usr/bin/python

import auto_generate_c

def jtag_decode(in_dict, f):
  
  data_dictionary = in_dict
  spl_init = [] #list for checking missed lines
  spl_fin = [] # ||

  for index in range(0, len(data_dictionary['TMS'])):
    if (data_dictionary['CST'][index] == '1')\
      and (data_dictionary['CST'][index+1] == '2')\
      and (data_dictionary['CST'][index+2] == '9')\
      and (data_dictionary['CST'][index+3] == '10')\
      \
      and (data_dictionary['CST'][index+12] == '12')\
      and (data_dictionary['CST'][index+13] == '15')\
      \
      and (data_dictionary['CST'][index+14] == '1')\
      and (data_dictionary['CST'][index+15] == '2')\
      and (data_dictionary['CST'][index+16] == '3')\
      \
      and (data_dictionary['CST'][index+49] == '5')\
      and (data_dictionary['CST'][index+50] == '6')\
      and (data_dictionary['CST'][index+51] == '7')\
      and (data_dictionary['CST'][index+52] == '4')\
      and (data_dictionary['CST'][index+53] == '5')\
      and (data_dictionary['CST'][index+54] == '8')\
      and (data_dictionary['CST'][index+55] == '1'):

      spl_init.append(int(data_dictionary['SPL'][index])) #adding spls for check
      spl_fin.append(int(data_dictionary['SPL'][index+55]))
      

      print 'Sample: '+data_dictionary['SPL'][index]+'->'\
      +data_dictionary['SPL'][index+55],'\tIR/DR ScanLong ',

      #put TDI/DO into a string
      tdi_ir = int(\
        (int(data_dictionary['TDI'][index+11])*128)+\
        (int(data_dictionary['TDI'][index+10])*64)+\
        (int(data_dictionary['TDI'][index+9])*32)+\
        (int(data_dictionary['TDI'][index+8])*16)+\
        (int(data_dictionary['TDI'][index+7])*8)+\
        (int(data_dictionary['TDI'][index+6])*4)+\
        (int(data_dictionary['TDI'][index+5])*2)+\
        (int(data_dictionary['TDI'][index+4])*1))
      print '\t',tdi_ir,


      tdi_dr = 0
      #48-45  
      if (data_dictionary['TDI'][index+48] == '1'):
        tdi_dr = tdi_dr + 0x8000000
      if (data_dictionary['TDI'][index+47] == '1'):
        tdi_dr = tdi_dr + 0x4000000
      if (data_dictionary['TDI'][index+46] == '1'):
        tdi_dr = tdi_dr + 0x2000000
      if (data_dictionary['TDI'][index+45] == '1'):
        tdi_dr = tdi_dr + 0x1000000
      #44-41
      if (data_dictionary['TDI'][index+44] == '1'):
        tdi_dr = tdi_dr + 0x800000
      if (data_dictionary['TDI'][index+43] == '1'):
        tdi_dr = tdi_dr + 0x400000
      if (data_dictionary['TDI'][index+42] == '1'):
        tdi_dr = tdi_dr + 0x200000
      if (data_dictionary['TDI'][index+41] == '1'):
        tdi_dr = tdi_dr + 0x100000
      #40-37
      if (data_dictionary['TDI'][index+40] == '1'):
        tdi_dr = tdi_dr + 0x80000
      if (data_dictionary['TDI'][index+39] == '1'):
        tdi_dr = tdi_dr + 0x40000
      if (data_dictionary['TDI'][index+38] == '1'):
        tdi_dr = tdi_dr + 0x20000
      if (data_dictionary['TDI'][index+37] == '1'):
        tdi_dr = tdi_dr + 0x10000
      #36-33
      if (data_dictionary['TDI'][index+36] == '1'):
        tdi_dr = tdi_dr + 0x8000
      if (data_dictionary['TDI'][index+35] == '1'):
        tdi_dr = tdi_dr + 0x4000
      if (data_dictionary['TDI'][index+34] == '1'):
        tdi_dr = tdi_dr + 0x2000
      if (data_dictionary['TDI'][index+33] == '1'):
        tdi_dr = tdi_dr + 0x1000
      #32-29
      if (data_dictionary['TDI'][index+32] == '1'):
        tdi_dr = tdi_dr + 0x800
      if (data_dictionary['TDI'][index+31] == '1'):
        tdi_dr = tdi_dr + 0x400
      if (data_dictionary['TDI'][index+30] == '1'):
        tdi_dr = tdi_dr + 0x2000
      if (data_dictionary['TDI'][index+29] == '1'):
        tdi_dr = tdi_dr + 0x1000
      #28-25
      if (data_dictionary['TDI'][index+28] == '1'):
        tdi_dr = tdi_dr + 0x800
      if (data_dictionary['TDI'][index+27] == '1'):
        tdi_dr = tdi_dr + 0x400
      if (data_dictionary['TDI'][index+26] == '1'):
        tdi_dr = tdi_dr + 0x200
      if (data_dictionary['TDI'][index+25] == '1'):
        tdi_dr = tdi_dr + 0x100
      #24-21
      if (data_dictionary['TDI'][index+24] == '1'):
        tdi_dr = tdi_dr + 0x80
      if (data_dictionary['TDI'][index+23] == '1'):
        tdi_dr = tdi_dr + 0x40
      if (data_dictionary['TDI'][index+22] == '1'):
        tdi_dr = tdi_dr + 0x20
      if (data_dictionary['TDI'][index+21] == '1'):
        tdi_dr = tdi_dr + 0x10
      #20-17
      if (data_dictionary['TDI'][index+20] == '1'):
        tdi_dr = tdi_dr + 0x8
      if (data_dictionary['TDI'][index+19] == '1'):
        tdi_dr = tdi_dr + 0x4
      if (data_dictionary['TDI'][index+18] == '1'):
        tdi_dr = tdi_dr + 0x2
      if (data_dictionary['TDI'][index+17] == '1'):
        tdi_dr = tdi_dr + 0x1

      print '\t',tdi_dr

      #generating c-code
      auto_generate_c.irdrscan(f,tdi_ir,tdi_dr)
      auto_generate_c.dr_exitl(f)


    elif (data_dictionary['CST'][index] == '1')\
      and (data_dictionary['CST'][index+1] == '2')\
      and (data_dictionary['CST'][index+2] == '9')\
      and (data_dictionary['CST'][index+3] == '10')\
      \
      and (data_dictionary['CST'][index+12] == '12')\
      and (data_dictionary['CST'][index+13] == '15')\
      \
      and (data_dictionary['CST'][index+14] == '1')\
      and (data_dictionary['CST'][index+15] == '2')\
      and (data_dictionary['CST'][index+16] == '3')\
      and (data_dictionary['CST'][index+17] == '4')\
      \
      and (data_dictionary['CST'][index+50] == '5')\
      and (data_dictionary['CST'][index+51] == '8'):

      spl_init.append(int(data_dictionary['SPL'][index])) #adding spls for check
      spl_fin.append(int(data_dictionary['SPL'][index+51])+1)

      print 'Sample: '+data_dictionary['SPL'][index]+'->'\
      +str(int(data_dictionary['SPL'][index+51])+1),'\tIR/DR ScanShort ',

      #put TDI/DO into a string
      tdi_ir = int(\
        (int(data_dictionary['TDI'][index+11])*128)+\
        (int(data_dictionary['TDI'][index+10])*64)+\
        (int(data_dictionary['TDI'][index+9])*32)+\
        (int(data_dictionary['TDI'][index+8])*16)+\
        (int(data_dictionary['TDI'][index+7])*8)+\
        (int(data_dictionary['TDI'][index+6])*4)+\
        (int(data_dictionary['TDI'][index+5])*2)+\
        (int(data_dictionary['TDI'][index+4])*1))
      print '\t',tdi_ir,


      tdi_dr = 0
      #48-45  
      if (data_dictionary['TDI'][index+48] == '1'):
        tdi_dr = tdi_dr + 0x8000000
      if (data_dictionary['TDI'][index+47] == '1'):
        tdi_dr = tdi_dr + 0x4000000
      if (data_dictionary['TDI'][index+46] == '1'):
        tdi_dr = tdi_dr + 0x2000000
      if (data_dictionary['TDI'][index+45] == '1'):
        tdi_dr = tdi_dr + 0x1000000
      #44-41
      if (data_dictionary['TDI'][index+44] == '1'):
        tdi_dr = tdi_dr + 0x800000
      if (data_dictionary['TDI'][index+43] == '1'):
        tdi_dr = tdi_dr + 0x400000
      if (data_dictionary['TDI'][index+42] == '1'):
        tdi_dr = tdi_dr + 0x200000
      if (data_dictionary['TDI'][index+41] == '1'):
        tdi_dr = tdi_dr + 0x100000
      #40-37
      if (data_dictionary['TDI'][index+40] == '1'):
        tdi_dr = tdi_dr + 0x80000
      if (data_dictionary['TDI'][index+39] == '1'):
        tdi_dr = tdi_dr + 0x40000
      if (data_dictionary['TDI'][index+38] == '1'):
        tdi_dr = tdi_dr + 0x20000
      if (data_dictionary['TDI'][index+37] == '1'):
        tdi_dr = tdi_dr + 0x10000
      #36-33
      if (data_dictionary['TDI'][index+36] == '1'):
        tdi_dr = tdi_dr + 0x8000
      if (data_dictionary['TDI'][index+35] == '1'):
        tdi_dr = tdi_dr + 0x4000
      if (data_dictionary['TDI'][index+34] == '1'):
        tdi_dr = tdi_dr + 0x2000
      if (data_dictionary['TDI'][index+33] == '1'):
        tdi_dr = tdi_dr + 0x1000
      #32-29
      if (data_dictionary['TDI'][index+32] == '1'):
        tdi_dr = tdi_dr + 0x800
      if (data_dictionary['TDI'][index+31] == '1'):
        tdi_dr = tdi_dr + 0x400
      if (data_dictionary['TDI'][index+30] == '1'):
        tdi_dr = tdi_dr + 0x2000
      if (data_dictionary['TDI'][index+29] == '1'):
        tdi_dr = tdi_dr + 0x1000
      #28-25
      if (data_dictionary['TDI'][index+28] == '1'):
        tdi_dr = tdi_dr + 0x800
      if (data_dictionary['TDI'][index+27] == '1'):
        tdi_dr = tdi_dr + 0x400
      if (data_dictionary['TDI'][index+26] == '1'):
        tdi_dr = tdi_dr + 0x200
      if (data_dictionary['TDI'][index+25] == '1'):
        tdi_dr = tdi_dr + 0x100
      #24-21
      if (data_dictionary['TDI'][index+24] == '1'):
        tdi_dr = tdi_dr + 0x80
      if (data_dictionary['TDI'][index+23] == '1'):
        tdi_dr = tdi_dr + 0x40
      if (data_dictionary['TDI'][index+22] == '1'):
        tdi_dr = tdi_dr + 0x20
      if (data_dictionary['TDI'][index+21] == '1'):
        tdi_dr = tdi_dr + 0x10
      #20-17
      if (data_dictionary['TDI'][index+20] == '1'):
        tdi_dr = tdi_dr + 0x8
      if (data_dictionary['TDI'][index+19] == '1'):
        tdi_dr = tdi_dr + 0x4
      if (data_dictionary['TDI'][index+18] == '1'):
        tdi_dr = tdi_dr + 0x2
      if (data_dictionary['TDI'][index+17] == '1'):
        tdi_dr = tdi_dr + 0x1

      print '\t',tdi_dr

      #generating c-code
      auto_generate_c.irdrscan(f,tdi_ir,tdi_dr)
      auto_generate_c.dr_exit(f)

  #check to see if any lines not covered by command
  for index in range(0, len(spl_fin)-1):
      if ((spl_init[index+1]-spl_fin[index]) > 1):
        print 'Error!',spl_init[index+1],spl_fin[index]
  return 0

#main
if __name__ == '__main__':
  
  import Open_Array

  input_file = 'temp_file.csv'
  data_dictionary = Open_Array.open_file_to_array(input_file)
#code for jtag
#"Globals"
  filename = 'auto_demo.c' 
  f = open(filename, 'wb')
  auto_generate_c.generate_header(f)

  auto_generate_c.generate_prototype('void','msr','int',f)
  auto_generate_c.generate_func('void','msr','int',f)
  auto_generate_c.close_func(f)

  auto_generate_c.generate_main(f)
  auto_generate_c.ftdi_setup(f)
  auto_generate_c.reset_chain(f)
  auto_generate_c.jtag_setup(f)
  auto_generate_c.run_test_idle(f)
  jtag_decode(data_dictionary, f)
  auto_generate_c.ftdi_close(f)
  auto_generate_c.close_main(f)
  f.close()
