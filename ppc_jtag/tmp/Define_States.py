#!/usr/bin/python

def define_states(in_dictionary):
  
#define the different states for the switch
  ST_TEST_LOGIC_RESET = 0
  ST_RUN_TEST_IDLE    = 1
  ST_SELECT_DR_SCAN   = 2
  ST_CAPTURE_DR       = 3
  ST_SHIFT_DR         = 4
  ST_EXIT1_DR         = 5
  ST_PAUSE_DR         = 6
  ST_EXIT2_DR         = 7
  ST_UPDATE_DR        = 8
  ST_SELECT_IR_SCAN   = 9
  ST_CAPTURE_IR       = 10
  ST_SHIFT_IR         = 11
  ST_EXIT1_IR         = 12
  ST_PAUSE_IR         = 13
  ST_EXIT2_IR         = 14
  ST_UPDATE_IR        = 15

#import in dictionary, add new columns, initialise state to reset
  data_dictionary = in_dictionary
  data_dictionary['C_STATE'] = [] 
  data_dictionary['F_STATE'] = []
  state = ST_TEST_LOGIC_RESET
  
#jtag state machine
  for index in range(0, len(data_dictionary['TMS'])):
    if state == ST_TEST_LOGIC_RESET:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '0':
        state = ST_RUN_TEST_IDLE
        data_dictionary['F_STATE'].insert(index, state)
      else:
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_RUN_TEST_IDLE:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_SELECT_DR_SCAN
        data_dictionary['F_STATE'].insert(index, state)
      else:
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_SELECT_DR_SCAN:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_SELECT_IR_SCAN
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_CAPTURE_DR
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_CAPTURE_DR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '0':
        state = ST_SHIFT_DR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_EXIT1_DR
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_SHIFT_DR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_EXIT1_DR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_EXIT1_DR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '0':
        state = ST_PAUSE_DR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_UPDATE_DR
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_PAUSE_DR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_EXIT2_DR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_EXIT2_DR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_UPDATE_DR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_SHIFT_DR
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_UPDATE_DR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_SELECT_DR_SCAN
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_RUN_TEST_IDLE
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_SELECT_IR_SCAN:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_TEST_LOGIC_RESET
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_CAPTURE_IR
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_CAPTURE_IR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '0':
        state = ST_SHIFT_IR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_EXIT1_IR
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_SHIFT_IR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_EXIT1_IR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_EXIT1_IR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '0':
        state = ST_PAUSE_IR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_UPDATE_IR
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_PAUSE_IR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_EXIT2_IR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_EXIT2_IR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_UPDATE_IR
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_SHIFT_IR
        data_dictionary['F_STATE'].insert(index, state)

    elif state == ST_UPDATE_IR:
      data_dictionary['C_STATE'].insert(index, state)
      if data_dictionary['TMS'][index] == '1':
        state = ST_SELECT_DR_SCAN
        data_dictionary['F_STATE'].insert(index, state)
      else:
        state = ST_RUN_TEST_IDLE
        data_dictionary['F_STATE'].insert(index, state)

    else:
      raise ValueError, 'unexpected input state: ' + state
#endof state machine
  #return dictionary
  return data_dictionary

def human_read_state(in_dictionary):
  
  '''human_read_state(dictionary)
  places strings defining the states into the dictionary'''

  data_dictionary = in_dictionary
  data_dictionary['HC_STATE'] = []
  data_dictionary['HF_STATE'] = []

  for index in range(0, len(data_dictionary['TMS'])):
    if data_dictionary['C_STATE'][index] == 0: data_dictionary['HC_STATE'].insert(index, 'ST_TEST_LOGIC_RESET')
    if data_dictionary['C_STATE'][index] == 1: data_dictionary['HC_STATE'].insert(index, 'ST_RUN_TEST_IDLE')
    if data_dictionary['C_STATE'][index] == 2: data_dictionary['HC_STATE'].insert(index, 'ST_SELECT_DR_SCAN')
    if data_dictionary['C_STATE'][index] == 3: data_dictionary['HC_STATE'].insert(index, 'ST_CAPTURE_DR')
    if data_dictionary['C_STATE'][index] == 4: data_dictionary['HC_STATE'].insert(index, 'ST_SHIFT_DR')
    if data_dictionary['C_STATE'][index] == 5: data_dictionary['HC_STATE'].insert(index, 'ST_EXIT1_DR')
    if data_dictionary['C_STATE'][index] == 6: data_dictionary['HC_STATE'].insert(index, 'ST_PAUSE_DR')
    if data_dictionary['C_STATE'][index] == 7: data_dictionary['HC_STATE'].insert(index, 'ST_EXIT2_DR')
    if data_dictionary['C_STATE'][index] == 8: data_dictionary['HC_STATE'].insert(index, 'ST_UPDATE_DR')
    if data_dictionary['C_STATE'][index] == 9: data_dictionary['HC_STATE'].insert(index, 'ST_SELECT_IR_SCAN')
    if data_dictionary['C_STATE'][index] == 10: data_dictionary['HC_STATE'].insert(index, 'ST_CAPTURE_IR')
    if data_dictionary['C_STATE'][index] == 11: data_dictionary['HC_STATE'].insert(index, 'ST_SHIFT_IR')
    if data_dictionary['C_STATE'][index] == 12: data_dictionary['HC_STATE'].insert(index, 'ST_EXIT1_IR')
    if data_dictionary['C_STATE'][index] == 13: data_dictionary['HC_STATE'].insert(index, 'ST_PAUSE_IR')
    if data_dictionary['C_STATE'][index] == 14: data_dictionary['HC_STATE'].insert(index, 'ST_EXIT2_IR')
    if data_dictionary['C_STATE'][index] == 15: data_dictionary['HC_STATE'].insert(index, 'ST_UPDATE_IR')

  for index in range(0, len(data_dictionary['TMS'])):
    if data_dictionary['F_STATE'][index] == 0: data_dictionary['HF_STATE'].insert(index, 'ST_TEST_LOGIC_RESET')
    if data_dictionary['F_STATE'][index] == 1: data_dictionary['HF_STATE'].insert(index, 'ST_RUN_TEST_IDLE')
    if data_dictionary['F_STATE'][index] == 2: data_dictionary['HF_STATE'].insert(index, 'ST_SELECT_DR_SCAN')
    if data_dictionary['F_STATE'][index] == 3: data_dictionary['HF_STATE'].insert(index, 'ST_CAPTURE_DR')
    if data_dictionary['F_STATE'][index] == 4: data_dictionary['HF_STATE'].insert(index, 'ST_SHIFT_DR')
    if data_dictionary['F_STATE'][index] == 5: data_dictionary['HF_STATE'].insert(index, 'ST_EXIT1_DR')
    if data_dictionary['F_STATE'][index] == 6: data_dictionary['HF_STATE'].insert(index, 'ST_PAUSE_DR')
    if data_dictionary['F_STATE'][index] == 7: data_dictionary['HF_STATE'].insert(index, 'ST_EXIT2_DR')
    if data_dictionary['F_STATE'][index] == 8: data_dictionary['HF_STATE'].insert(index, 'ST_UPDATE_DR')
    if data_dictionary['F_STATE'][index] == 9: data_dictionary['HF_STATE'].insert(index, 'ST_SELECT_IR_SCAN')
    if data_dictionary['F_STATE'][index] == 10: data_dictionary['HF_STATE'].insert(index, 'ST_CAPTURE_IR')
    if data_dictionary['F_STATE'][index] == 11: data_dictionary['HF_STATE'].insert(index, 'ST_SHIFT_IR')
    if data_dictionary['F_STATE'][index] == 12: data_dictionary['HF_STATE'].insert(index, 'ST_EXIT1_IR')
    if data_dictionary['F_STATE'][index] == 13: data_dictionary['HF_STATE'].insert(index, 'ST_PAUSE_IR')
    if data_dictionary['F_STATE'][index] == 14: data_dictionary['HF_STATE'].insert(index, 'ST_EXIT2_IR')
    if data_dictionary['F_STATE'][index] == 15: data_dictionary['HF_STATE'].insert(index, 'ST_UPDATE_IR')
  
  return data_dictionary

#main
if __name__ == '__main__':

  import Open_Array

  input_file = 'edit_msr000.csv'
  data_dictionary = Open_Array.open_file_to_array(input_file)
  #print data_dictionary
  appended_data_dict = define_states(data_dictionary)
  appended_data_dict_2 = human_read_state(appended_data_dict)
  print appended_data_dict_2

#endof main
