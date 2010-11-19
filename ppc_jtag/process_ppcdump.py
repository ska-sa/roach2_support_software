#!/usr/bin/python

import struct,sys
import string
import csv
import numpy as N
import array


def reverse(s):
  aa = array.array('c',s)
  aa.reverse()
  return aa.tostring()

class PPCDump(object):
  """PowerPC signal dump class"""
  command = ''
  tdi = []
  tdo = []
  tms = []
  trst = []
  halt = []
  r_tags = []
  def __init__(self, command):
    self.command = command;

  def str_indexof(self, arr, match):
    for i in range(len(arr)):
      if (arr[i].upper().strip() == match.upper()):
        return i;
    return -1

  def parse_csv_file(self,f):
    parser = csv.reader(f)
    first = True

    table_header = []
    table_values = []
    for fields in parser:
      if first:
        table_header = fields
        first = False
      else:
        table_values.append([int (moo) for moo in fields])

    data = N.array(table_values)
    if (self.str_indexof(table_header, 'TDI') >= 0) :
      self.tdi = data[:,self.str_indexof(table_header, 'TDI')];
    if (self.str_indexof(table_header, 'TDO') >= 0) :
      self.tdo = data[:,self.str_indexof(table_header, 'TDO')];
    if (self.str_indexof(table_header, 'TMS') >= 0) :
      self.tms = data[:,self.str_indexof(table_header, 'TMS')];
    if (self.str_indexof(table_header, 'TRST') >= 0) :
      self.trst = data[:,self.str_indexof(table_header, 'TRST')];
    if (self.str_indexof(table_header, 'HALT') >= 0) :
      self.halt = data[:,self.str_indexof(table_header, 'HALT')];

  def tag_r_ops(self,init_state=0):
    # this code will kill kittens
    TEST_LOGIC_RESET = 0
    RUN_TEST_IDLE    = 1
    SELECT_DR_SCAN   = 2
    CAPTURE_DR       = 3
    SHIFT_DR         = 4
    EXIT1_DR         = 5
    PAUSE_DR         = 6
    EXIT2_DR         = 7
    UPDATE_DR        = 8
    SELECT_IR_SCAN   = 9
    CAPTURE_IR       = 10
    SHIFT_IR         = 11
    EXIT1_IR         = 12
    PAUSE_IR         = 13
    EXIT2_IR         = 14
    UPDATE_IR        = 15

    prev_state = 0;
    state = init_state
    index = 0;
    # python seems to append arrays by reference so need current_tag to be defined in loop!?!
    madness = [0,0,0]
    self.rtags = []

    prev_trst=1
    prev_halt=1

    for tms in self.tms:
      state_before = state;
      current_tag = [madness[0], madness[1], madness[2]]

      if self.halt[index] != prev_halt :
        #default is set
        event = [2, 0, 0];
        if (self.halt(index)) :
          #cleared (active low)
          event = [3, 0, 0];

        self.r_tags.append(event);
      prev_halt = self.halt[index]

      if self.trst[index] != prev_trst :
        #default is set
        event = [4, 0, 0];
        if (self.trst(index)) :
          #cleared (active low)
          event = [5, 0, 0];

        self.r_tags.append(event);
      prev_trst = self.trst[index]

      if   (state == TEST_LOGIC_RESET) :
        if (prev_state != TEST_LOGIC_RESET) :
          event = [6, 0, 0];
          self.r_tags.append(event);

        if (tms):
          state = TEST_LOGIC_RESET;
        else :
          state = RUN_TEST_IDLE;
      elif (state == RUN_TEST_IDLE) :
        if (tms):
          state = SELECT_DR_SCAN;
        else :
          state = RUN_TEST_IDLE;
      elif (state == SELECT_DR_SCAN) :
        if (tms):
          state = SELECT_IR_SCAN;
        else :
          state = CAPTURE_DR;
      elif (state == CAPTURE_DR) :
        if (tms):
          state = EXIT1_DR;
        else :
          state = SHIFT_DR;
      elif (state == SHIFT_DR) :
        if (tms):
          state = EXIT1_DR;
          current_tag[2] = index
        else :
          state = SHIFT_DR;

        if (prev_state != SHIFT_DR) :
          current_tag[0] = 0
          current_tag[1] = index

      elif (state == EXIT1_DR) :
        if (tms):
          state = UPDATE_DR;
        else :
          state = PAUSE_DR;
      elif (state == PAUSE_DR) :
        if (tms):
          state = EXIT2_DR;
        else :
          state = PAUSE_DR;
      elif (state == EXIT2_DR) :
        if (tms):
          state = UPDATE_DR;
        else :
          state = SHIFT_DR;
      elif (state == UPDATE_DR) :
        self.r_tags.append(current_tag);
        if (tms):
          state = SELECT_DR_SCAN;
        else :
          state = RUN_TEST_IDLE;
      elif (state == SELECT_IR_SCAN) :
        if (tms):
          state = TEST_LOGIC_RESET;
        else :
          state = CAPTURE_IR;
      elif (state == CAPTURE_IR) :
        if (tms):
          state = EXIT1_IR;
        else :
          state = SHIFT_IR;
      elif (state == SHIFT_IR) :
        if (tms):
          state = EXIT1_IR;
          current_tag[2] = index
        else :
          state = SHIFT_IR;

        if (prev_state != SHIFT_IR) :
          current_tag[0] = 1
          current_tag[1] = index

      elif (state == EXIT1_IR) :
        if (tms):
          state = UPDATE_IR;
        else :
          state = PAUSE_IR;
      elif (state == PAUSE_IR) :
        if (tms):
          state = EXIT2_IR;
        else :
          state = PAUSE_IR;
      elif (state == EXIT2_IR) :
        if (tms):
          state = UPDATE_IR;
        else :
          state = SHIFT_IR;
      elif (state == UPDATE_IR) :

        self.r_tags.append(current_tag);
        if (tms):
          state = SELECT_DR_SCAN;
        else :
          state = RUN_TEST_IDLE;
      else :
        print 'error: invalid state'
        return;

      prev_state = state_before
      index += 1
      madness = current_tag
    return;

  def dump_ops_in(self):
    for ctag in self.r_tags:
      if (ctag[0] == 0) :
        print 'DR ',
      elif (ctag[0] == 1) :
        print 'IR ',
      elif (ctag[0] == 2) :
        print 'HALT SET'
        break
      elif (ctag[0] == 3) :
        print 'HALT CLEARED'
        break
      elif (ctag[0] == 4) :
        print 'TRST SET'
        break
      elif (ctag[0] == 5) :
        print 'TRST CLEARED'
        break
      elif (ctag[0] == 6) :
        print 'JTAG LOGIC RESET'
        break
      else: 
        break

      s=''
      for val in self.tdi[ctag[1]:ctag[2]+1] :
        s+='%d'%(val)
      print '%s'%(reverse(s))

  def dump_ops_full(self):
    for ctag in self.r_tags:
      if (ctag[0] == 0) :
        print 'DR ',
      elif (ctag[0] == 1) :
        print 'IR ',
      elif (ctag[0] == 2) :
        print 'HALT SET'
        break
      elif (ctag[0] == 3) :
        print 'HALT CLEARED'
        break
      elif (ctag[0] == 4) :
        print 'TRST SET'
        break
      elif (ctag[0] == 5) :
        print 'TRST CLEARED'
        break
      else: 
        break

      print '[%d]'%(ctag[2]-ctag[1] + 1)

      print 'TDI: ', 
      s=''
      for val in self.tdi[ctag[1]:ctag[2]+1] :
        s+='%d'%(val)
      print '%s'%(reverse(s))

      print 'TDO: ', 
      s=''
      for val in self.tdo[ctag[1]+1:ctag[2]+2] :
        s+='%d'%(val)
      print '%s'%(reverse(s))

def get_command(filename):
  slashpos = filename.rfind('/');
  if (slashpos >= 0 ):
    filename = filename[slashpos+1:]
  dumppos = filename.find('dump-');
  if (dumppos != 0):
    return '';
  dotpos = filename.find('.csv');
  if (dumppos < 0):
    return '';
  trans = string.maketrans('_',' ')
  pretrans = filename[5:dotpos]
  return pretrans.translate(trans)

exit = 0
try:
  if sys.argv[1] == '-h':
    print "usage: process_ppcdump [dumpfile]"
    exit=1
except:
  print "usage: process_ppcdump [dumpfile]"
  exit=1

if exit:
  sys.exit(1)

filename=sys.argv[1]

fid = open(filename,'r')

command = get_command(filename)

if (command == ''):
  print 'error: dump file name does not comply with specification, couldn\'t extract command'
  sys.exit(1)

ppcdump = PPCDump(command)

ppcdump.parse_csv_file(fid)

ppcdump.tag_r_ops()

ppcdump.dump_ops_in()

fid.close()

