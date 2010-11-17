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
      and (data_dictionary['CST'][index+13] == '15'):

      spl_init.append(int(data_dictionary['SPL'][index])) #adding spls for check
      spl_fin.append(int(data_dictionary['SPL'][index+13]))
      

      print 'Sample: '+data_dictionary['SPL'][index]+'->'\
      +data_dictionary['SPL'][index+13],'IR Scan '\
      '\nTDI: '\
      +data_dictionary['TDI'][index+11]\
      +data_dictionary['TDI'][index+10]\
      +data_dictionary['TDI'][index+9]\
      +data_dictionary['TDI'][index+8]\
      +data_dictionary['TDI'][index+7]\
      +data_dictionary['TDI'][index+6]\
      +data_dictionary['TDI'][index+5]\
      +data_dictionary['TDI'][index+4]

      print 'TDO: '\
      +data_dictionary['TDO'][index+11]\
      +data_dictionary['TDO'][index+10]\
      +data_dictionary['TDO'][index+9]\
      +data_dictionary['TDO'][index+8]\
      +data_dictionary['TDO'][index+7]\
      +data_dictionary['TDO'][index+6]\
      +data_dictionary['TDO'][index+5]\
      +data_dictionary['TDO'][index+4]


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


      spl_init.append(int(data_dictionary['SPL'][index])) #adding spls for check
      spl_fin.append(int(data_dictionary['SPL'][index+41]))
      
      print 'Sample: '+data_dictionary['SPL'][index]+'->'\
      +data_dictionary['SPL'][index+41],'DR Scan '\
      +'\nTDI: '\
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

      print 'TDO: '\
      +data_dictionary['TDO'][index+35]\
      +data_dictionary['TDO'][index+34]\
      +data_dictionary['TDO'][index+33]\
      +data_dictionary['TDO'][index+32]\
      +data_dictionary['TDO'][index+31]\
      +data_dictionary['TDO'][index+30]\
      +data_dictionary['TDO'][index+29]\
      +data_dictionary['TDO'][index+28]+' '\
      +data_dictionary['TDO'][index+27]\
      +data_dictionary['TDO'][index+26]\
      +data_dictionary['TDO'][index+25]\
      +data_dictionary['TDO'][index+24]\
      +data_dictionary['TDO'][index+23]\
      +data_dictionary['TDO'][index+22]\
      +data_dictionary['TDO'][index+21]\
      +data_dictionary['TDO'][index+20]+' '\
      +data_dictionary['TDO'][index+19]\
      +data_dictionary['TDO'][index+18]\
      +data_dictionary['TDO'][index+17]\
      +data_dictionary['TDO'][index+16]\
      +data_dictionary['TDO'][index+15]\
      +data_dictionary['TDO'][index+14]\
      +data_dictionary['TDO'][index+13]\
      +data_dictionary['TDO'][index+12]+' '\
      +data_dictionary['TDO'][index+11]\
      +data_dictionary['TDO'][index+10]\
      +data_dictionary['TDO'][index+9]\
      +data_dictionary['TDO'][index+8]\
      +data_dictionary['TDO'][index+7]\
      +data_dictionary['TDO'][index+6]\
      +data_dictionary['TDO'][index+5]\
      +data_dictionary['TDO'][index+4]

    elif (data_dictionary['CST'][index] == '1')\
      and (data_dictionary['CST'][index+1] == '2')\
      and (data_dictionary['CST'][index+2] == '3')\
      and (data_dictionary['CST'][index+3] == '4')\
      \
      and (data_dictionary['CST'][index+36] == '5')\
      and (data_dictionary['CST'][index+37] == '8')\
      and (data_dictionary['FST'][index+37] == '1'):

      spl_init.append(int(data_dictionary['SPL'][index])) #adding spls for check
      spl_fin.append(int(data_dictionary['SPL'][index+37]))

      print 'Sample: '+data_dictionary['SPL'][index]+'->'\
      +data_dictionary['SPL'][index+37],'DR Scan(2) '\
      +'\nTDI: '\
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
      
      print 'TDO: '\
      +data_dictionary['TDO'][index+35]\
      +data_dictionary['TDO'][index+34]\
      +data_dictionary['TDO'][index+33]\
      +data_dictionary['TDO'][index+32]\
      +data_dictionary['TDO'][index+31]\
      +data_dictionary['TDO'][index+30]\
      +data_dictionary['TDO'][index+29]\
      +data_dictionary['TDO'][index+28]+' '\
      +data_dictionary['TDO'][index+27]\
      +data_dictionary['TDO'][index+26]\
      +data_dictionary['TDO'][index+25]\
      +data_dictionary['TDO'][index+24]\
      +data_dictionary['TDO'][index+23]\
      +data_dictionary['TDO'][index+22]\
      +data_dictionary['TDO'][index+21]\
      +data_dictionary['TDO'][index+20]+' '\
      +data_dictionary['TDO'][index+19]\
      +data_dictionary['TDO'][index+18]\
      +data_dictionary['TDO'][index+17]\
      +data_dictionary['TDO'][index+16]\
      +data_dictionary['TDO'][index+15]\
      +data_dictionary['TDO'][index+14]\
      +data_dictionary['TDO'][index+13]\
      +data_dictionary['TDO'][index+12]+' '\
      +data_dictionary['TDO'][index+11]\
      +data_dictionary['TDO'][index+10]\
      +data_dictionary['TDO'][index+9]\
      +data_dictionary['TDO'][index+8]\
      +data_dictionary['TDO'][index+7]\
      +data_dictionary['TDO'][index+6]\
      +data_dictionary['TDO'][index+5]\
      +data_dictionary['TDO'][index+4]

  #check to see if any lines not covered by command
  for index in range(0, len(spl_fin)-1):
      if ((spl_init[index+1]-spl_fin[index]) > 2):
        print spl_init[index+1],spl_fin[index]
  return 0

#main
if __name__ == '__main__':
  
  import Open_Array

  input_file = 'temp_file.csv'
  data_dictionary = Open_Array.open_file_to_array(input_file)
  jtag_decode(data_dictionary)
