#!/usr/bin/python

def jtag_decode(in_dict):
  
  data_dictionary = in_dict

  for index in range(0, len(data_dictionary['TMS'])):
    if (data_dictionary['CST'][index] == '1')\
      and (data_dictionary['CST'][index+1] == '2')\
      and (data_dictionary['CST'][index+2] == '9')\
      and (data_dictionary['CST'][index+3] == '10')\
      \
      and (data_dictionary['CST'][index+12] == '12')\
      and (data_dictionary['CST'][index+13] == '15'):

      print 'Sample: '+data_dictionary['SPL'][index],'to '\
      +data_dictionary['SPL'][index+13],'IR Scan '\
      'TDI: '\
      +data_dictionary['TDI'][index+4]\
      +data_dictionary['TDI'][index+5]\
      +data_dictionary['TDI'][index+6]\
      +data_dictionary['TDI'][index+7]\
      +data_dictionary['TDI'][index+8]\
      +data_dictionary['TDI'][index+9]\
      +data_dictionary['TDI'][index+10]\
      +data_dictionary['TDI'][index+11]

    elif (data_dictionary['CST'][index] == '1')\
      and (data_dictionary['CST'][index+1] == '2')\
      and (data_dictionary['CST'][index+2] == '3')\
      and (data_dictionary['CST'][index+3] == '4')\
      \
      and (data_dictionary['CST'][index+36] == '6')\
      and (data_dictionary['CST'][index+37] == '7')\
      and (data_dictionary['CST'][index+38] == '4')\
      and (data_dictionary['CST'][index+39] == '5')\
      and (data_dictionary['CST'][index+40] == '8')\
      and (data_dictionary['CST'][index+41] == '1'):

      print 'Sample: '+data_dictionary['SPL'][index],'to '\
      +data_dictionary['SPL'][index+41],'DR Scan '\
      +data_dictionary['TDI'][index+35]\
      +data_dictionary['TDI'][index+34]\
      +data_dictionary['TDI'][index+33]\
      +data_dictionary['TDI'][index+32]\
      +data_dictionary['TDI'][index+31]\
      +data_dictionary['TDI'][index+30]\
      +data_dictionary['TDI'][index+29]\
      +data_dictionary['TDI'][index+28]+' '\
      +data_dictionary['TDI'][index+27]\
      +data_dictionary['TDI'][index+26]\
      +data_dictionary['TDI'][index+25]\
      +data_dictionary['TDI'][index+24]\
      +data_dictionary['TDI'][index+23]\
      +data_dictionary['TDI'][index+22]\
      +data_dictionary['TDI'][index+21]\
      +data_dictionary['TDI'][index+20]+' '\
      +data_dictionary['TDI'][index+19]\
      +data_dictionary['TDI'][index+18]\
      +data_dictionary['TDI'][index+17]\
      +data_dictionary['TDI'][index+16]\
      +data_dictionary['TDI'][index+15]\
      +data_dictionary['TDI'][index+14]\
      +data_dictionary['TDI'][index+13]\
      +data_dictionary['TDI'][index+12]+' '\
      +data_dictionary['TDI'][index+11]\
      +data_dictionary['TDI'][index+10]\
      +data_dictionary['TDI'][index+9]\
      +data_dictionary['TDI'][index+8]\
      +data_dictionary['TDI'][index+7]\
      +data_dictionary['TDI'][index+6]\
      +data_dictionary['TDI'][index+5]\
      +data_dictionary['TDI'][index+4]

    elif (data_dictionary['CST'][index] == '1')\
      and (data_dictionary['CST'][index+1] == '2')\
      and (data_dictionary['CST'][index+2] == '3')\
      and (data_dictionary['CST'][index+3] == '4')\
      \
      and (data_dictionary['CST'][index+36] == '5')\
      and (data_dictionary['CST'][index+37] == '8')\
      and (data_dictionary['FST'][index+37] == '1'):

      print 'Sample: '+data_dictionary['SPL'][index],'to '\
      +data_dictionary['SPL'][index+37],'DR Scan(2) '\
      +data_dictionary['TDI'][index+35]\
      +data_dictionary['TDI'][index+34]\
      +data_dictionary['TDI'][index+33]\
      +data_dictionary['TDI'][index+32]\
      +data_dictionary['TDI'][index+31]\
      +data_dictionary['TDI'][index+30]\
      +data_dictionary['TDI'][index+29]\
      +data_dictionary['TDI'][index+28]+' '\
      +data_dictionary['TDI'][index+27]\
      +data_dictionary['TDI'][index+26]\
      +data_dictionary['TDI'][index+25]\
      +data_dictionary['TDI'][index+24]\
      +data_dictionary['TDI'][index+23]\
      +data_dictionary['TDI'][index+22]\
      +data_dictionary['TDI'][index+21]\
      +data_dictionary['TDI'][index+20]+' '\
      +data_dictionary['TDI'][index+19]\
      +data_dictionary['TDI'][index+18]\
      +data_dictionary['TDI'][index+17]\
      +data_dictionary['TDI'][index+16]\
      +data_dictionary['TDI'][index+15]\
      +data_dictionary['TDI'][index+14]\
      +data_dictionary['TDI'][index+13]\
      +data_dictionary['TDI'][index+12]+' '\
      +data_dictionary['TDI'][index+11]\
      +data_dictionary['TDI'][index+10]\
      +data_dictionary['TDI'][index+9]\
      +data_dictionary['TDI'][index+8]\
      +data_dictionary['TDI'][index+7]\
      +data_dictionary['TDI'][index+6]\
      +data_dictionary['TDI'][index+5]\
      +data_dictionary['TDI'][index+4]
  return 0

#main
if __name__ == '__main__':
  
  import Open_Array

  input_file = 'temp_file.csv'
  data_dictionary = Open_Array.open_file_to_array(input_file)
  jtag_decode(data_dictionary)
