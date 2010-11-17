def write_dict_to_csv(in_dict, filename):
  
  import csv #for csv.write
  import string #for strip

  data_dictionary = in_dict
  file_in = open(filename, 'wb')
  write_file = csv.writer(file_in)
  write_file.writerow(['SPL', 'TMS', 'TDI', 'TDO', 'CST', 'FST'])

  for index in range(0, len(data_dictionary['TMS'])):
    write_file.writerow([data_dictionary['SAMPLE'][index],\
    data_dictionary['TMS'][index],\
    data_dictionary['TDI'][index],\
    #strip get rid of space
    string.strip(data_dictionary['TDO'][index]),\
    #wont append int and string, so need typecast
    str(data_dictionary['C_STATE'][index]),\
    str(data_dictionary['F_STATE'][index])])

  file_in.close()
  return 1

def hwrite_dict_to_csv(in_dict, filename):

  import csv
  import string

  data_dictionary = in_dict
  file_in = open(filename, 'wb')
  write_file = csv.writer(file_in, dialect='excel')
  write_file.writerow(['SPL', 'TMS', 'TDI', 'TDO', 'CST', 'FST', 'HCST', 'HFST'])

  for index in range(0, len(data_dictionary['TMS'])):
     write_file.writerow([data_dictionary['SAMPLE'][index],\
     data_dictionary['TMS'][index],\
     data_dictionary['TDI'][index],\
     #strip get rid of space
     string.strip(data_dictionary['TDO'][index]),\
     #for appending,wont append str&int
     str(data_dictionary['C_STATE'][index]),\
     str(data_dictionary['F_STATE'][index]),\
     data_dictionary['HC_STATE'][index],\
     data_dictionary['HF_STATE'][index]])
    
  file_in.close()
  return 1

#main
if __name__ == '__main__':

  import Open_Array
  import Define_States
  import string

  input_file = 'edit_pc_000.txt' #'edit_msr000.csv'
  data_dictionary = Open_Array.open_file_to_array(input_file)
  appended_data_dict = Define_States.define_states(data_dictionary)
  appended_data_dict_2 = Define_States.human_read_state(appended_data_dict)
  hwrite_dict_to_csv(appended_data_dict_2, 'pc.csv')

  print 'SPL,TMS,TDI,TDO,CST,CST,FST,FST'
  for index in range(0, len(appended_data_dict_2['TMS'])):
    print appended_data_dict_2['SAMPLE'][index]+','+\
          appended_data_dict_2['TMS'][index]+','+\
          appended_data_dict_2['TDI'][index]+','+\
          string.strip(appended_data_dict_2['TDO'][index])+','+\
          str(appended_data_dict_2['C_STATE'][index])+','+\
          appended_data_dict_2['HC_STATE'][index]+','+\
          str(appended_data_dict_2['F_STATE'][index])+','+\
          appended_data_dict_2['HF_STATE'][index]
  #print appended_data_dict_2


