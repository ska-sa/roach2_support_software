#!/usr/bin/python

import sys

'''  urJTAG defines '''

URJTAG_PROGRAMMER = "roach-2"
URJTAG_PROGRAMMER_PARAMETERS = ""
BSDL_PATH = "/home/dave/work/svnROACH2/testing/bsdl"

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

# mess with dbcr0
PPCMODE_DEBUG_RESET = "110111000000000000000000000000000"
PPCMODE_DEBUG_EXTERNAL = "110000000000000000000000000000000"
PPCMODE_DEBUG_READ = "010000000000000000000000000000000"


# Hmmm, that would make sense except for below'
PPCMODE_SYNC = "000000000000000000000000001010100"

PPCMODE_GO0  = "100000000000000000000000000000000"
PPCMODE_GO1  = "000000000000000000000000000000000"

PPCMODE_STEP0 = "110100000000000000000000000000000"
PPCMODE_STEP1 = "010100000000000000000000000000000"

PPCDBGR_READ = "000000000000000000000000010110100"

PPC_MMUSETUP = 0x01040000

''' Instuction Dictionaries '''

MAJ_OPCODE = {'xtend': 31,
              'xtendl': 19,
              'addis': 15,
              'stwu': 37,
              'ori': 24,
              'lwz': 32}

EXT_OPCODE = {'mfspr': 339,
              'mtspr': 467,
              'mfmsr': 83,
              'mtmsr': 146,
              'tlbwe': 978,
              'bclr': 16}

SPRF = {'dbdr': 0x3f3, # data debug register 
        'mmucr': 0x3b2, # mmu control register
        'lr': 0x08} # Link register control register

# TODO: global optimization, dont change ppc insturction if dont need to 
# TODO: need to restore registers that are changed (ie MSR, MMU, LR...)

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

def gen_xlform_inst(opcode, XO, regmaj, regmid, regmin, lk=0):
  return int2bin( ((opcode & 0x3f) << 26) |
                  ((regmaj & 0x1f) << 21) |
                  ((regmid & 0x1f) << 16) |
                  ((regmin & 0x1f) << 11) |
                  ((XO & 0x3ff) << 1) | 
                  (lk & 0x1)
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

def ppc_set_pc(addr, reg):
  # write the value into the debug register
  print "instruction PPCDBGR"
  print "shift ir"
  print "dr 1%s"%(int2bin(addr,32))
  print "shift dr"
  # load the value from the debug register into ppc register
  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mfspr'], reg, SPRF['dbdr']))
  print "shift dr"
  # load the value from the ppc register to the link register
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mtspr'], reg, SPRF['lr']))
  print "shift dr"
  # branch to location in lr
  print "dr 1%s"%(gen_xlform_inst(MAJ_OPCODE['xtendl'], EXT_OPCODE['bclr'], 20, 0, 0, 0))
  print "shift dr"

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

def ppc_fetch_spr(spr, datareg):

  #load selected spr into datareg
  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mfspr'], datareg, spr))
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
  print "dr 1%s"%(gen_xfxform_inst(MAJ_OPCODE['xtend'], EXT_OPCODE['mtspr'], reg, spr))
  print "shift dr"

def ppc_load_mem_to_reg(address, reg_addr, reg_data):
  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_dform_inst(MAJ_OPCODE['addis'], reg_addr, 0, (address & 0xffff0000) >> 16))
  print "shift dr"
  print "dr 1%s"%(gen_dform_inst(MAJ_OPCODE['ori'], reg_addr, reg_addr, (address & 0xffff)))
  print "shift dr"
  print "dr 1%s"%(gen_dform_inst(MAJ_OPCODE['lwz'], reg_data, reg_addr, 0))
  print "shift dr"


def ppc_load_reg_to_mem(reg_addr, reg_data, address):
  value = address
  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_dform_inst(MAJ_OPCODE['addis'], reg_addr, 0, (value & 0xffff0000) >> 16))
  print "shift dr"
  print "dr 1%s"%(gen_dform_inst(MAJ_OPCODE['ori'], reg_addr, reg_addr, (value & 0xffff)))
  print "shift dr"
  print "dr 1%s"%(gen_dform_inst(MAJ_OPCODE['stwu'], reg_data, reg_addr, 0x0))
  print "shift dr"

  
  
def ppc_set_cpu_reg(value, reg):
  value_bin = int2bin(value,32)
  reg_bin = int2bin(reg,5)
  """
  # This code not the optimal solution
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
  """

  print "instruction PPCINST"
  print "shift ir"
  print "dr 1%s"%(gen_dform_inst(MAJ_OPCODE['addis'], reg, 0, (value & 0xffff0000) >> 16))
  print "shift dr"
  print "dr 1%s"%(gen_dform_inst(MAJ_OPCODE['ori'], reg, reg, (value & 0xffff)))
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
  print "reading register %d"%(reg)
  print "dr"

def ppc_setup_mmu(reg):
  ppc_set_spr(SPRF['mmucr'], PPC_MMUSETUP, reg)


''' macro equivalent operations '''

def init_jtag():
  print "cable %s %s"%(URJTAG_PROGRAMMER,URJTAG_PROGRAMMER_PARAMETERS)
  if (BSDL_PATH != "") :
    print "bsdl path %s"%(BSDL_PATH)
  print "detect"
  print "register R_PPCMODE %d"%(JTAGD_LENGTH)
  print "register R_PPCINST %d"%(JTAGD_LENGTH)
  print "register R_PPCDBGR %d"%(JTAGD_LENGTH)
  print "instruction length %d"%(JTAGI_LENGTH)
  print "instruction PPCMODE %s R_PPCMODE"%(JTAGI_PPCMODE)
  print "instruction PPCINST %s R_PPCINST"%(JTAGI_PPCINST)
  print "instruction PPCDBGR %s R_PPCDBGR"%(JTAGI_PPCDBGR)

def run_halt(command, args):
  # first halt the processor
  print "pod HALT=1"

  # select the PPCMODE instruction
  print "instruction PPCMODE"
  # load instruction
  print "shift ir"
  print "dr %s"%(PPCMODE_DEBUG_EXTERNAL)
  print "shift dr"

  # clear the halt flag
  print "pod HALT=0"

  print "shift ir"
  print "dr %s"%(PPCMODE_DEBUG_EXTERNAL)
  print "shift dr"

def run_reset(command, args):
  # halt the processor
  print "pod HALT=1"

  # select the PPCMODE instruction
  print "instruction PPCMODE"
  # load instruction
  print "shift ir"
  print "dr %s"%(PPCMODE_DEBUG_RESET)
  print "shift dr"
  print "shift ir"
  print "dr %s"%(PPCMODE_DEBUG_EXTERNAL)
  print "shift dr"

  # unhalt the processor
  print "pod HALT=0"

  print "shift ir"
  print "dr %s"%(PPCMODE_DEBUG_EXTERNAL)
  print "shift dr"
  print "dr %s"%(PPCMODE_DEBUG_READ)
  print "shift dr"
  print "shift ir"
  print "dr %s"%(PPCMODE_SYNC)
  print "shift dr"

  # TODO: setup/store MMU
  ppc_setup_mmu(1)


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
  print "#%s %s"%(command,args)
  raw=args.lower()
  if (raw == ""):
    print "fixme: pc read not implemented"
    return;


  addr = hex2dec(raw)

  ppc_set_pc(addr, 1)

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

def run_spr(command, args):
  print "#%s %s"%(command,args)
  raw=args.lower()
  parts=raw.partition(' = ')

  if (parts[2] == ""):
    # spr to get
    spr = hex2dec(parts[0])
    # register to store the spr that is fetched
    reg_data = 1
    ppc_fetch_spr(spr, reg_data)
    ppc_get_cpu_reg(reg_data)
    return
  
  spr = hex2dec(parts[0])
  data = hex2dec(parts[2])

  ppc_set_spr(spr, data, 1)


def run_word(command, args):
  print "#%s %s"%(command,args)
  raw=args.lower()
  parts=raw.partition(' = ')

  if (parts[2] == ""):
    # address of data to fetch
    address = parts[0]
    # register to load the address to fetch
    reg_addr = 2
    # register to store the data that is fetched
    reg_data = 1
    ppc_load_mem_to_reg(hex2dec(parts[0]),reg_addr,reg_data)
    ppc_get_cpu_reg(reg_data)
    return
  
  address = hex2dec(parts[0])
  data = hex2dec(parts[2])

  ppc_set_cpu_reg(data, 0)

  ppc_load_reg_to_mem(1, 0, address)


def run_go(command, args):
  # select the PPCMODE instruction
  print "# %s %s"%(command,args)
  print "instruction PPCMODE"
  # perform magic sequence

  print "shift ir"
  print "dr %s"%(PPCMODE_SYNC)
  print "shift dr"
  print "shift ir"
  print "dr %s"%(PPCMODE_SYNC)
  print "shift dr"

  print "shift ir"
  print "dr %s"%(PPCMODE_GO0)
  print "shift dr"
  print "dr %s"%(PPCMODE_GO1)
  print "shift dr"

  print "shift ir"
  print "dr %s"%(PPCMODE_SYNC)
  print "shift dr"
  print "shift ir"
  print "dr %s"%(PPCMODE_SYNC)
  print "shift dr"

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
    ["spr",   run_spr],
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

