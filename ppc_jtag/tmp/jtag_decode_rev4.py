#!/usr/bin/python

def jtag_decode(in_dict):
  
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
      +data_dictionary['SPL'][index+55],'IR/DR ScanLong '\


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
      +str(int(data_dictionary['SPL'][index+51])+1),'IR/DR ScanShort '\

  #check to see if any lines not covered by command
  for index in range(0, len(spl_fin)-1):
      if ((spl_init[index+1]-spl_fin[index]) > 1):
        print spl_init[index+1],spl_fin[index]
  return 0

#main
if __name__ == '__main__':
  
  import Open_Array

  input_file = 'temp_file.csv'
  data_dictionary = Open_Array.open_file_to_array(input_file)
  jtag_decode(data_dictionary)
