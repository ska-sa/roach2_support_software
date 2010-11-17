#main
if __name__ == '__main__':
  
  from Open_Array import *
  from Define_States import *
  from print_dict import *
  from string import *

  input_file = 'edit_pc_000.txt'
  data_dictionary = open_file_to_array(input_file)
  appended_data_dict = define_states(data_dictionary)
  appended_data_dict_2 = human_read_state(appended_data_dict)
  hwrite_dict_to_csv(appended_data_dict_2, 'pc.csv')

  print 'SPL,TMS,TDI,TDO,CST,CST,FST,FST'
  for index in range(0, len(appended_data_dict_2['TMS'])):
    print appended_data_dict_2['SAMPLE'][index]+','+\
          appended_data_dict_2['TMS'][index]+','+\
          appended_data_dict_2['TDI'][index]+','+\
          strip(appended_data_dict_2['TDO'][index])+','+\
          str(appended_data_dict_2['C_STATE'][index])+','+\
          appended_data_dict_2['HC_STATE'][index]+','+\
          str(appended_data_dict_2['F_STATE'][index])+','+\
          appended_data_dict_2['HF_STATE'][index]

  input_file = 'edit_msr000.txt'
  data_dictionary = open_file_to_array(input_file)
  appended_data_dict = define_states(data_dictionary)
  appended_data_dict_2 = human_read_state(appended_data_dict)
  hwrite_dict_to_csv(appended_data_dict_2, 'msr.csv')

  print 'SPL,TMS,TDI,TDO,CST,CST,FST,FST'
  for index in range(0, len(appended_data_dict_2['TMS'])):
    print appended_data_dict_2['SAMPLE'][index]+','+\
          appended_data_dict_2['TMS'][index]+','+\
          appended_data_dict_2['TDI'][index]+','+\
          strip(appended_data_dict_2['TDO'][index])+','+\
          str(appended_data_dict_2['C_STATE'][index])+','+\
          appended_data_dict_2['HC_STATE'][index]+','+\
          str(appended_data_dict_2['F_STATE'][index])+','+\
          appended_data_dict_2['HF_STATE'][index]

  input_file = 'edit_word_000.txt'
  data_dictionary = open_file_to_array(input_file)
  appended_data_dict = define_states(data_dictionary)
  appended_data_dict_2 = human_read_state(appended_data_dict)
  hwrite_dict_to_csv(appended_data_dict_2, 'word.csv')

  print 'SPL,TMS,TDI,TDO,CST,CST,FST,FST'
  for index in range(0, len(appended_data_dict_2['TMS'])):
    print appended_data_dict_2['SAMPLE'][index]+','+\
          appended_data_dict_2['TMS'][index]+','+\
          appended_data_dict_2['TDI'][index]+','+\
          strip(appended_data_dict_2['TDO'][index])+','+\
          str(appended_data_dict_2['C_STATE'][index])+','+\
          appended_data_dict_2['HC_STATE'][index]+','+\
          str(appended_data_dict_2['F_STATE'][index])+','+\
          appended_data_dict_2['HF_STATE'][index]


  input_file = 'edit_wtlb0_000.txt'
  data_dictionary = open_file_to_array(input_file)
  appended_data_dict = define_states(data_dictionary)
  appended_data_dict_2 = human_read_state(appended_data_dict)
  hwrite_dict_to_csv(appended_data_dict_2, 'wtlb0.csv')

  print 'SPL,TMS,TDI,TDO,CST,CST,FST,FST'
  for index in range(0, len(appended_data_dict_2['TMS'])):
    print appended_data_dict_2['SAMPLE'][index]+','+\
          appended_data_dict_2['TMS'][index]+','+\
          appended_data_dict_2['TDI'][index]+','+\
          strip(appended_data_dict_2['TDO'][index])+','+\
          str(appended_data_dict_2['C_STATE'][index])+','+\
          appended_data_dict_2['HC_STATE'][index]+','+\
          str(appended_data_dict_2['F_STATE'][index])+','+\
          appended_data_dict_2['HF_STATE'][index]



