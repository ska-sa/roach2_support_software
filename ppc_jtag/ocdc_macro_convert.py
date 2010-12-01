#!/usr/bin/python

import sys

'''  urJTAG defines '''

URJTAG_PROGRAMMER = "jtagkey"
URJTAG_PROGRAMMER_PARAMETERS = ""

''' PPC JTAG defines '''

#PPC JTAG instruction length
JTAGI_LENGTH = 8
#PPC JTAG data length
JTAGD_LENGTH = 33
#JTAG PPCMODE instruction code (Used to set JTAG debug mode)
JTAGI_PPCMODE = "01010100"
#JTAG PPCINST instruction code (Used to run PPC instructions presented in data words)
JTAGI_PPCINST = "01110100"
#JTAG PPCDBGR instruction code (Used to read and write to the DEBUG special register)
JTAGI_PPCDBGR = "10110100"

''' PPC JTAG magic strings '''

PPCMODE_INIT0 = "110111000000000000000000000000000"
PPCMODE_INIT1 = "110000000000000000000000000000000"
PPCMODE_INIT2 = "110000000000000000000000000000000"
PPCMODE_INIT3 = "010000000000000000000000000000000"

PPCMODE_SYNC = "000000000000000000000000001010100"

PPCMODE_GO0  = "100000000000000000000000000000000"
PPCMODE_GO1  = "000000000000000000000000000000000"

PPCMODE_STEP0 = "110100000000000000000000000000000"
PPCMODE_STEP1 = "010100000000000000000000000000000"

PPCDBGR_READ = "000000000000000000000000010110100"

''' Instuction Dictionaries '''
MAJ_OPCODE = {'xtend': 31,
              'addis': 15}
EXT_OPCODE = {'mfspr': 339,
              'mtspr': 475,
              'mfmsr': 83,
              'mtmsr': 146,
              'tlbwe': 978}
SPRF = {'dbdr': 0x3f3, # data debug register 
        'mmucr': 0x3b2} # mmu control register


''' Misc functions '''

def hex2dec(s):
  parts=s.partition('0x')
  value=0
  if (parts[2] != ""):
    value = int(parts[2], 16)
  else:
    value = int(parts[0])
  return value

def int2bin(n, count=32):
  """returns the binary of integer n, using count number of digits"""
  return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

def gen_dform_inst(opcode, regmaj, regmin, data):
  return int2bin( ((opcode & 0x3f) << 26) |
                  ((regmaj & 0x1f) << 21) |
                  ((regmin & 0x1f) << 16) |
                  ((data & 0xffff)) 
                 )

def gen_xform_inst(opcode, XO, regmaj, regmid, regmin, rc=0):
  return int2bin( ((opcode & 0x3f) << 26) |
                  ((regmaj & 0x1f) << 21) |
                  ((regmid & 0x1f) << 16) |
                  ((regmin & 0x1f) << 11) |
                  ((XO & 0x3ff) << 1) | 
                  (rc & 0x1)
                 )

def gen_xfxform_inst(opcode, XO, regmaj, sprf):
  # sprf is split into two parts, swapped
  return int2bin( ((opcode & 0x3f) << 26) |
                  ((regmaj & 0x1f) << 21) |
                  ((sprf & 0x01f) << 16) |
                  (((sprf & 0x3e0)>>5) << 11) |
                  ((XO & 0x3ff) << 1) 
                 )

''' Common PPC Tasks '''

def ppc_tlb_write(val, tlbindex, reg):
  for i in range(0,3):
    # write the value into the debug register
    print "instruction PPCDBGR"
    print "shift ir"
    print "dr 1%s"%(int2bin(val[i],32))
    print "shift dr"
    # load the value from the debug register into ppc register
    print "instruction PPCINST"
    print "shift ir"
    print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mfspr'], reg, SPRF['dbdr']))
    print "shift dr"
    # Set up the TLB
    print "dr 1%s"%(gen_xform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['tlbwe'], reg, tlbindex, i))
    print "shift dr"

def ppc_set_msr(value, reg):
  value_bin = int2bin(value,32)
  reg_bin = int2bin(reg,5)
  # write the value into the debug register
  print "instruction PPCDBGR"
  print "shift ir"
  print "dr 1%s"%(value_bin)
  print "shift dr"
  # load the value from the debug register into ppc register
  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mfspr'], reg, SPRF['dbdr']))
  print "shift dr"
  # load the value from the debug register into ppc register
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mtmsr'], reg, 0))
  print "shift dr"

def ppc_set_spr(spr, value, reg):
  value_bin = int2bin(value,32)
  reg_bin = int2bin(reg,5)
  # write the value into the debug register
  print "instruction PPCDBGR"
  print "shift ir"
  print "dr 1%s"%(value_bin)
  print "shift dr"
  # load the value from the debug register into ppc register
  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mfspr'], reg, SPRF['dbdr']))
  print "shift dr"
  # load the value from the debug register into ppc register
  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mtspr'], reg, spr))
  print "shift dr"

def ppc_set_cpu_reg(value, reg):
  value_bin = int2bin(value,32)
  reg_bin = int2bin(reg,5)
  # write the value into the debug register
  print "instruction PPCDBGR"
  print "shift ir"
  print "dr 1%s"%(value_bin)
  print "shift dr"
  # load the value from the debug register into ppc register
  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mfspr'], reg, SPRF['dbdr']))
  print "shift dr"

def ppc_get_cpu_reg(reg):
  reg_bin = int2bin(reg,5)
  # load the value from the ppc register into debug register
  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mtspr'], reg, SPRF['dbdr']))
  print "shift dr"
  # dump the value out of the debug register
  print "instruction PPCDBGR"
  print "shift ir"
  print "dr %s"%(PPCDBGR_READ)
  print "shift dr"
  print "dr"

''' macro equivalent operations '''

def init_jtag():
  print "cable %s %s"%(URJTAG_PROGRAMMER,URJTAG_PROGRAMMER_PARAMETERS)
  print "detect"
  print "register R_PPCMODE %d"%(JTAGD_LENGTH)
  print "register R_PPCINST %d"%(JTAGD_LENGTH)
  print "register R_PPCDBGR %d"%(JTAGD_LENGTH)
  print "intruction length %d"%(JTAGI_LENGTH)
  print "instruction PPCMODE %s R_PPCMODE"%(JTAGI_PPCMODE)
  print "instruction PPCINST %s R_PPCINST"%(JTAGI_PPCINST)
  print "instruction PPCDBGR %s R_PPCDBGR"%(JTAGI_PPCDBGR)

def run_reset(command, args):
  # first clear the halt flag, wait a bit then set it
  print "pod reset=1"
  print "usleep 10000"
  print "pod reset=0"

  # select the PPCMODE instruction
  print "instruction PPCMODE"
  # load instruction
  print "ir"
  print "dr %s"%(PPCMODE_INIT0)
  print "shift dr"
  print "dr %s"%(PPCMODE_INIT1)
  print "shift dr"

  # clear the halt flag
  print "pod reset=1"

  print "dr %s"%(PPCMODE_INIT2)
  print "shift dr"
  print "dr %s"%(PPCMODE_INIT3)
  print "shift dr"
  print "dr %s"%(PPCMODE_SYNC)
  print "shift dr"

  # TODO: setup/store MMU


def run_wtlb(command, args):
  print "#%s %s"%(command,args)
  val = [0,0,0]
  tlb_index = 0
  unknown = 0

  parts = args.partition(' ')
  tlb_index = hex2dec(parts[0])
  parts = parts[2].partition(' ')
  val[0] = hex2dec(parts[0])
  parts = parts[2].partition(' ')
  unknown = hex2dec(parts[0])
  parts = parts[2].partition(' ')
  val[1] = hex2dec(parts[0])
  parts = parts[2].partition(' ')
  val[2] = hex2dec(parts[0])

  ppc_tlb_write(val,tlb_index,1)

def run_pc(command, args):
  print "#(TO BE IMPLEMENTED) - %s %s"%(command,args)

def run_msr(command, args):
  print "#%s %s"%(command,args)
  raw=args.lower()
  parts=raw.partition('= ')
  noequals=""
  if (parts[2] != ""):
    noequals = parts[2]
  else:
    noequals = parts[0]

  parts=noequals.partition('0x')
  value=0
  if (parts[2] != ""):
    value = int(parts[2], 16)
  else:
    value = int(parts[0])
    
  ppc_set_msr(value, 1)

def run_cpu(command, args):
  print "#(NOT IMPLEMENTED) - %s %s"%(command,args)

def run_word(command, args):
  print "#(TO BE IMPLEMENTED) - %s %s"%(command,args)

def run_go(command, args):
  # TODO: clear MSR
  print command

def run_exit(command, args):
  #this command does nothing
  print "",

def get_operation(opmap, opstring):
  ret=0
  for op in opmap:
    if op[0].lower() == opstring.lower():
      ret = op[1]
  return ret

"""
------------------ MAIN LOOP -----------------
"""

exit = 0
try:
  if sys.argv[1] == '-h':
    print "usage: ocdc_macro_convert [file]"
    exit=1
except:
  print "usage: ocdc_macro_convert [file]"
  exit=1

if exit:
  sys.exit(1)

fid = open(sys.argv[1],'r')

operation_map = [
    ["reset", run_reset],
    ["wtlb",  run_wtlb],
    ["pc",    run_pc],
    ["msr",   run_msr],
    ["cpu",   run_cpu],
    ["word",  run_word],
    ["go",    run_go],
    ["exit",  run_exit]
  ]

init_jtag()

for c in fid.readlines():
  cmd_parts = c.partition(" ")
  if (c == ""):
    continue
  if (c[0] == "#" or c[0] == ";"):
    continue
  if (c.rstrip("\n ") == ""):
    continue

  op = cmd_parts[0].rstrip("\n ");
  arg = cmd_parts[2].rstrip("\n ");
  operation = get_operation(operation_map, op)
  if operation:
    operation(op, arg)
  else:
    print "#unknown operation: %s %s"%(op,arg)

fid.close()

