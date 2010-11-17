def generate_main(f):
  '''Writes c main header etc. Also includes #defines. Remember to close!'''

  f.write('#include <stdio.h>\n\
#include <ftdi.h>\n\
\n\
#define VENDOR 0x0403\n\
#define PRODUCT 0x6010\n\
\n\
int main(void)\n\
{\n')

def close_main(f):
  '''Closes c main header.'''

  f.write('}\n')

def ftdi_setup(f):
  '''Setup the ftdi chip for JTAG.'''
  f.write('  struct ftdi_context ftdi_context; //handle for device\n\
  int ftdi_status = -1; //result of each call\n\
\n\
  struct ftdi_device_list *no_devices = 0; //number of devices\n\
  unsigned int dev_index = 0xF; //device in the list used\n\
\n\
  unsigned char out_buffer[1024]; //output buffer, commands sent to ft2232h\n\
  int i = 0; //initialze buffer to 0\n\
  for (i = 0; i < 1024; i++)\n\
  {\n\
    out_buffer[i] = 0;\n\
  }\n\
  unsigned char in_buffer[1024]; //input buffer, hold data from ft2232h\n\
  for (i = 0; i < 1024; i++) //initialise buffer to 0\n\
  {\n\
    in_buffer[i] = 0;\n\
  }\n\
\n\
  int count = 0; //general loop index\n\
  int num_bytes_to_send = 0; //index for output buffer\n\
  int num_bytes_sent = 0; //count of actual bytes sent - used with write\n\
  int num_bytes_to_read = 0; //number of bytes available to read in drivers input buffer\n\
  int num_bytes_read = 0; //count of actual bytes read - used with read\n\
  int clock_divisor = 0x05DB; //vaulue of clock divisor, scl freq = 60/((1+0x05DB)*2)(MHz)=20KHz\n\
\n\
  /*------------------------------------------------------------------------*/\n\
  //does ftdi device exist?\n\
  printf("Checking for FTDI devices...\\n");\n\
  ftdi_status = ftdi_usb_find_all(&ftdi_context, &no_devices, VENDOR, PRODUCT);\n\
  if (ftdi_status < 0) //did command execute ok?\n\
  {\n\
    printf("Error in getting number of devices\\n");\n\
    return 1;  //exit with error\n\
  }\n\
  if (no_devices < 1) //exit if we dont see any\n\
  {\n\
    printf("There are no FTDI devices installed\\n");\n\
    return 1; //exit with error\n\
  }\n\
  printf("%s FTDI devices found - the count includes individual ports on a single chip\\n",no_devices);\n\
\n\
  /*--------------------------------------------------------------------------\n\
   * Open the port\n\
   *------------------------------------------------------------------------*/\n\
\n\
  //initialise a ftdi context\n\
  printf("Initialising FTDI context...\\n");\n\
  ftdi_status = ftdi_init(&ftdi_context);\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
    {\n\
      printf("couldn\'t allocate read buffer\\n");\n\
      return 1; //exit with error\n\
    }\n\
    else\n\
    {\n\
      printf("undefined error: %d\\n", ftdi_status);\n\
      return 1; //exit with error\n\
    }\n\
  }\n\
\n\
  //open ftdi device\n\
  printf("Opening FTDI device...\\n");\n\
  ftdi_status = ftdi_usb_open(&ftdi_context, VENDOR, PRODUCT);\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
    {\n\
      printf("Error: %d, usb_find_busses() failed\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -2)\n\
    {\n\
      printf("Error: %d, usb_find_devices() failed\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -3)\n\
    {\n\
      printf("Error: %d, usb device not found\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -4)\n\
    {\n\
      printf("Error: %d, unable to open device\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -5)\n\
    {\n\
      printf("Error; %d, unable to claim device\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -6)\n\
    {\n\
      printf("Error: %d, reset failed\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -7)\n\
    {\n\
      printf("Error: %d, set baudrate failed\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -8)\n\
    {\n\
      printf("Error: %d, get product description failed\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -9)\n\
    {\n\
      printf("Error: %d, get serial number failed\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -10)\n\
    {\n\
      printf("Error: %d, unable to close device\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else\n\
    {\n\
      printf("Error: %d, undefined error: %d\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
  }\n\
\n\
  //configure the port parameters\n\
  printf("Configuring port for MPSSE use...\\n");\n\
  ftdi_status = ftdi_usb_reset(&ftdi_context);//reset usb\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
    {\n\
      printf("Error: %d, FTDI reset failed\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else if (ftdi_status == -2)\n\
    {\n\
      printf("Error: %d, USB device unavailable\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
    else\n\
    {\n\
      printf("Error: %d, undefined error\\n", ftdi_status);\n\
      return 1;\n\
    }\n\
  }\n\
\n\
  //set usb transfer sizes to 64k\n\
  ftdi_status = ftdi_write_data_set_chunksize(&ftdi_context, 65536);\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
      printf("Error: %d, ftdi context invalid\\n", ftdi_status);\n\
    else\n\
      printf("Error: %d, undefined error\\n", ftdi_status);\n\
  }\n\
\n\
  //disable event and error characters\n\
  ftdi_status = ftdi_set_event_char(&ftdi_context, 0, 0);\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
      printf("Error: %d, unable to set event character\\n", ftdi_status);\n\
    else if (ftdi_status == -2)\n\
      printf("Error: %d, USB device unavailable\\n", ftdi_status);\n\
    else\n\
      printf("Error: %d, undefined error\\n", ftdi_status);\n\
  }\n\
  ftdi_status = ftdi_set_error_char(&ftdi_context, 0, 0);\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
      printf("Error: %d, unable to set error character\\n", ftdi_status);\n\
    else if (ftdi_status == -2)\n\
      printf("Error: %d, USB device unavailable\\n", ftdi_status);\n\
    else\n\
      printf("Error: %d, undefined error\\n", ftdi_status);\n\
  }\n\
\n\
  //set the read and write timouts in milliseconds\n\
  printf("READ AND WRITE TIMEOUTS STILL NEED TO BE SET...\\n");\n\
\n\
  //set the latency timer to 16ms\n\
  ftdi_status = ftdi_set_latency_timer(&ftdi_context, 16);\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
      printf("Error: %d, latency out of range\\n", ftdi_status);\n\
    else if (ftdi_status == -2)\n\
      printf("Error: %d, unable to set latency timer\\n", ftdi_status);\n\
    else if (ftdi_status == -3)\n\
      printf("Error: %d, USB device unavailable\\n", ftdi_status);\n\
    printf("Error: %d, undefined error\\n", ftdi_status);\n\
  }\n\
\n\
  //reset controller\n\
  ftdi_status = ftdi_set_bitmode(&ftdi_context, 0x00, BITMODE_RESET);\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
      printf("Error: %d, can\'t enable bitbang mode\\n", ftdi_status);\n\
    else if (ftdi_status == -2)\n\
      printf("Error: %d, USB device unavailable\\n", ftdi_status);\n\
    else\n\
      printf("Error, undefined error\\n", ftdi_status);\n\
  }\n\
\n\
  //enable mpsse mode\n\
  ftdi_status = ftdi_set_bitmode(&ftdi_context, 0x00, BITMODE_MPSSE);\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
      printf("Error: %d, can\'t enable bitbang mode\\n", ftdi_status);\n\
    else if (ftdi_status == -2)\n\
      printf("Error: %d, USB device unavailable\\n", ftdi_status);\n\
    else\n\
      printf("Error: %d, undefined error\\n", ftdi_status);\n\
  }\n\
  printf("Sleeping for 1.\\n");\n\
  sleep(1); //wait for all the usb stuff to complete\n\
\n\
  /*------------------------------------------------------------------------*/\n\n')

def ftdi_close(f):
  '''Close the chip and context.'''

  f.write('  /*-------------------------------------------------------------------------\n\
  * Start closing everything down\n\
  *------------------------------------------------------------------------*/\n\
\n\
  printf("\\nJTAG program executed successfully. \\n");\n\
  printf("Press <Enter> to continue\\n");\n\
  getchar(); //wait for a carriage return\n\
\n\
  //attempt to close ftdi device\n\
  ftdi_status = ftdi_usb_close(&ftdi_context);\n\
  if (ftdi_status != 0)\n\
  {\n\
    if (ftdi_status == -1)\n\
      printf("usb_release failed\\n");\n\
    else if (ftdi_status == -2)\n\
      printf("usb_close failed\\n");\n\
    else if (ftdi_status == -3)\n\
      printf("ftdi context invalid\\n");\n\
    else\n\
      printf("Undefined error: %d\\n", ftdi_status);\n\
  }\n\
\n\
  //deinitialize a ftdi_context\n\
  ftdi_deinit(&ftdi_context);\n\
\n\
  printf("FTDI chip closed and ftdi context deinitialized. \\n");\n\
  //printf("Press <Enter> to terminate\\n");\n\
  //getchar();\n\
  printf("Goodbye...\\n");\n\
  return 0;\n\n')

def jtag_setup(f):
  '''Configure the MPSSE settigns for JTAG, multiple commands can be sent
  to the MPSSE using 1 write command'''

  f.write('  num_bytes_to_send = 0; //zero the index\n\
\n\
  //set up the high speed specific commands for ft2232h\n\
\n\
  out_buffer[num_bytes_to_send++] = 0x8A; //use 60 MHz master clk(disable /5)\n\
  out_buffer[num_bytes_to_send++] = 0x97; //turn off adaptive clocking\n\
  out_buffer[num_bytes_to_send++] = 0x8D; //disable 3 phase clocking\n\
\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send); //send of the high speed commands\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  // Set initial states of the MPSSE interface - low byte(lsb), both pin durections and output values\n\
  // Pin name    Signal    Direction    Config    Initial State    Config\n\
  // ADBUS0      TCK       Output       1         low              0\n\
  // ADBUS1      TDI       Output       1         low              0\n\
  // ADBUS2      TDO       Input        0                          0\n\
  // ADBUS3      TMS       Output       1         high?            1\n\
  // ADBUS4      GPIOL0    Input        0                          0\n\
  // ADBUS5      GPIOL1    Input        0                          0\n\
  // ADBUS6      GPIOL2    Input        0                          0\n\
  // ADBUS7      GPIOL3    Input        0                          0\n\
\n\
  printf("Setting initial states...\\n");\n\
  out_buffer[num_bytes_to_send++] = 0x80; //set data bytes low\n\
  out_buffer[num_bytes_to_send++] = 0x08; //initial state config above(1000)\n\
  out_buffer[num_bytes_to_send++] = 0x0B; //direction config above(1011)\n\
\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off the low GPIO config commands\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  // Set initial states of the MPSSE interface - high byte, both pin directions and output values\n\
  // Pin name    Signal    Direction    Config    Initial State    Config\n\
  // ACBUS0      GPIOH0    Input        0                          0\n\
  // ACBUS1      GPIOH1    Input        0                          0\n\
  // ACBUS2      GPIOH2    Input        0                          0\n\
  // ACBUS3      GPIOH3    Input        0                          0\n\
  // ACBUS4      GPIOH4    Input        0                          0\n\
  // ACBUS5      GPIOH5    Input        0                          0\n\
  // ACBUS6      GPIOH6    Input        0                          0\n\
  // ACBUS7      GPIOH7    Input        0                          0\n\
\n\
  out_buffer[num_bytes_to_send++] = 0x82; //set data bytes high\n\
  out_buffer[num_bytes_to_send++] = 0x00; //initial state config above(0000)\n\
  out_buffer[num_bytes_to_send++] = 0x00; //direction config above(0000)\n\
\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off the low GPIO config commands\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  //set TCK frequency\n\
  //TCK = 60MHz/((1+[(1+0xValueH*256) OR 0xValueL])*2)\n\
  out_buffer[num_bytes_to_send++] = \'\\x86\'; //command to set clock divisor\n\
  out_buffer[num_bytes_to_send++] = (clock_divisor & 0xFF);//set 0xValueL of clock divisor\n\
  out_buffer[num_bytes_to_send++] = ((clock_divisor >> 8)& 0xFF);//set 0xValueH of clock divisor\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off the low GPIO config commands\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  //disable internal loopback\n\
  out_buffer[num_bytes_to_send++] = 0x85; //disable loopback\n\
  //loopback is when tdi/do are internally connected for testing\n\
\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off loopback command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\n')

def reset_chain(f):
  '''Universal reset command.'''

  f.write('  num_bytes_to_send = 0; //zero the index\n\
\n\
  out_buffer[num_bytes_to_send++] = 0x4B; //clock data to tms pin(noread)\n\
  out_buffer[num_bytes_to_send++] = 5;\n\
  out_buffer[num_bytes_to_send++] = 0x9F; //tms: 10011111\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);\n\
    //send reset command off\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\n')

def bogus_command(f):
  '''Non-defined command used to generate an error.'''

  f.write('  num_bytes_to_send = 0; //reset output buffer\n\
  out_buffer[num_bytes_to_send++] = 0xAA; //add bogus command 0xAA to queue\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);\n\
    //send off the bad commands\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  ftdi_status = ftdi_read_data(&ftdi_context, in_buffer, 1024); //read 32 bytes(arb)\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_read().\\n");\n\
  else if (ftdi_status == 0)\n\
    printf("no data was available\\n");\n\n')

def run_test_idle(f):
  '''Goto run test idle state'''

  f.write('\
  // navigate TMS through test-logic-reset->run-test-idle\n\
  //                                        TMS=0\n\
  out_buffer[num_bytes_to_send++] = 0x4B; //dont read data in test-logic-reset, run-test-idle\n\
  out_buffer[num_bytes_to_send++] = 0x00; //number of clock pulses = length+1(1 clock here)\n\
  out_buffer[num_bytes_to_send++] = 0x00; //data is shifted LSB first, so TMS pattern is 0\n\
\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n')

def irdrscan(f,irdi, drdi):
  '''Run through irscan and drscan.'''
  
  f.write('\
  // navigate TMS through run-test-idle->select-DR-scan->select-IR-scan->capture-IR->shift-IR\n\
  //                                     TMS=1           TMS=1           TMS=0       TMS=0\n\
  out_buffer[num_bytes_to_send++] = 0x4B; //dont read data in run-test-idle, select-dr-scan, select-ir-scan\n\
  out_buffer[num_bytes_to_send++] = 0x03; //number of clock pulses = length+1(4 clocks here)\n\
  out_buffer[num_bytes_to_send++] = 0x03; //data is shifted LSB first, so TMS pattern is 1100\n\
                                          //bit 7 is 0 therefore DO/TDI will be 0 for entire duration\n\
\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  // TMS is currently 0. State machine is in Shift-IR, so now use the TDI/TDO command to shift data into TDI/DO while reading TDO/DI\n\
  // Although 8 bits shifted in, only need 7 clocks here. The 8th will be in conjunction with the TMS command, coming next\n\
\n\
  out_buffer[num_bytes_to_send++] = 0x3B; //clock data out through states Capture-IR, Shift-IR and Exit-IR, read back result\n\
  out_buffer[num_bytes_to_send++] = 0x06; //number of clock pulses = length + 1 (7 clocks here)\n\
  out_buffer[num_bytes_to_send++] = '+str(hex(irdi))+'; //shift out data (ignore last bit)\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  // here is the TMS command for 1 clock. Data is also shifted in.\n\
\n\
  out_buffer[num_bytes_to_send++] = 0x6B; //clock out TMS, read 1 bit.\n\
  out_buffer[num_bytes_to_send++] = 0x00; //number of pulses = length + 0 (1 here)\n\
  out_buffer[num_bytes_to_send++] = 0x03 & ('+str(hex(irdi))+' & 0x80); //11000000&irdi&00000001\n\
  //data is shifted lsb first, so TMS becomes 1, also, bit 7 is shifted into TDI/DO,\n\
  //the 1 in bit 1 will leave TMS high for the next commands.\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  //navigate TMS from Exit-IR through Update-IR->Run-Test-Idle->Select-DR-Scan->Capture-DR->Shift-DR\n\
  //                                  TMS=1      TMS=0          TMS=1           TMS=0       TMS=0\n\
\n\
  out_buffer[num_bytes_to_send++] = 0x4B; // don\'t read data in Update-IR->Run-Test-Idle->Select-DR-Scan->Capture-DR\n\
  out_buffer[num_bytes_to_send++] = 0x04; //no of clock pulses = length+1(5 clks here)\n\
  out_buffer[num_bytes_to_send++] = 0x05; //data is shifted lsb first, so TMS pattern is 10100\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  //navigate TMS from Exit-IR through Update-IR->Select-DR-Scan->Capture-DR->Shift-DR\n\
  //                                  TMS=1      TMS=1           TMS=0       TMS=0\n\
//\n\
  //out_buffer[num_bytes_to_send++] = 0x4B; // don\'t read data in update-ir->select-dr-scan->capture-dr\n\
  //out_buffer[num_bytes_to_send++] = 0x03; //no of clock pulses = length+1(4 clks here)\n\
  //out_buffer[num_bytes_to_send++] = 0x83; //data is shifted lsb first, so TMS pattern is 1100\n\
  //ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  //if (ftdi_status == -666)\n\
  //  printf("USB device unavailable.\\n");\n\
  //else if (ftdi_status < 0)\n\
  //  printf("error code from usb_bulk_write().\\n");\n\
//\n\
  //num_bytes_to_send = 0; //reset output buffer\n\
\n\
  // TMS is currently low. State Machine is in Shift-DR, so now use the TDI/TDO command to shift drdi out TDI/DO while reading TDO/DI\n\
  // Although 32 bits need shifted in, only 31 are clocked here. The 32nd will be in conjunction with the TMS command. coming next\n\
\n\
  out_buffer[num_bytes_to_send++] = 0x3B; //clock data out through states shift-dr and exit-dr\n\
  out_buffer[num_bytes_to_send++] = 0x1E; //no. of clock pulses=length+1(31 clocks here)\n\
  out_buffer[num_bytes_to_send++] = '+str(hex(drdi))+'; //shift out 31bits(ignore last bit)\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  // Here is the TMS command for one clock. Data is also shifted in.\n\
\n\
  out_buffer[num_bytes_to_send++] = 0x6B; //clock out tms, read 1 bit\n\
  out_buffer[num_bytes_to_send++] = 0x00; //no. of clock pulses=length+1(1 clocks here)\n\
  out_buffer[num_bytes_to_send++] = 0xC0000000 & ('+str(hex(drdi))+' & 0x80000000);\n\
                                         //data is shifted lsb 1st, so tms becomes 1. also, bit 31 is shifted into tdi/do, also a 1\n\
                                         //the 1 in bit 1 will leave tms high for next commands\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n')

def dr_exit(f):
  '''Simple shift from DR Regitser to Run Test Idle'''

  f.write('\
  // Navigate through Update-DR->Run-Test-Idle->Run-Test-Idle\n\
  //                  TMS=1      TMS=0          TMS=0\n\
\n\
  out_buffer[num_bytes_to_send++] = 0x4B; //don\'t read data in Update-DR->Run-Test-Idle->Run-Test-Idle\n\
  out_buffer[num_bytes_to_send++] = 0x02; //no. of clock pulses=length+1(3 clocks here)\n\
  out_buffer[num_bytes_to_send++] = 0x01; //data is shifted lsb first, so tms pattern is 100\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  ftdi_status = ftdi_read_data(&ftdi_context, in_buffer, 1024); //read 32 bytes(arb)\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_read().\\n");\n\
  else if (ftdi_status == 0)\n\
    printf("no data was available\\n");\n\
\n')

def dr_exitl(f):
  '''Alternative shift from DR Register to Run Test Idle'''

  f.write('\
  // Navigate from Exit1-DR->Pause-DR->Exit2-DR->Shift-DR\n\
  //                         TMS=0     TMS=1     TMS=0\n\
  out_buffer[num_bytes_to_send++] = 0x4B; //don\'t read data in Exit1-DR->Pause-DR->Exit2-DR->Shift-DR\n\
  out_buffer[num_bytes_to_send++] = 0x02; //no. of clock pulses=length+1(3 clocks here)\n\
  out_buffer[num_bytes_to_send++] = 0x02; //data is shifted lsb first, so tms pattern is 010\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  // Navigate from Shift-DR->Exit1-DR->Update-DR\n\
  //                         TMS=1     TMS=1\n\
  out_buffer[num_bytes_to_send++] = 0x4B; //don\'t read data in Shift-DR->Exit1-DR->Update-DR\n\
  out_buffer[num_bytes_to_send++] = 0x01; //no. of clock pulses=length+1(2 clocks here)\n\
  out_buffer[num_bytes_to_send++] = 0x83; //data is shifted lsb first, so tms pattern is 11\n\
                                          //the 1 on bit 7 will keep DO/TDI high\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  // Navigate from Update-DR->Run-Test-Idle->Run-Test-Idle\n\
  //                          TMS=0          TMS=0\n\
  out_buffer[num_bytes_to_send++] = 0x4B; //don\'t read data in Update-DR->Run-Test-Idle->Run-Test-Idle\n\
  out_buffer[num_bytes_to_send++] = 0x01; //no. of clock pulses=length+1(2 clocks here)\n\
  out_buffer[num_bytes_to_send++] = 0x00; //data is shifted lsb first, so tms pattern is 00\n\
                                          //bit 7 is zero->DO/TDI is zero\n\
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_write().\\n");\n\
\n\
  num_bytes_to_send = 0; //reset output buffer\n\
\n\
  ftdi_status = ftdi_read_data(&ftdi_context, in_buffer, 1024); //read 32 bytes(arb)\n\
  if (ftdi_status == -666)\n\
    printf("USB device unavailable.\\n");\n\
  else if (ftdi_status < 0)\n\
    printf("error code from usb_bulk_read().\\n");\n\
  else if (ftdi_status == 0)\n\
    printf("no data was available\\n");\n\
\n')

def dr_reset(f):

  fwrite('\
  // Navigate through Update-DR->Select-DR-Scan->Select-IR-Scan->Test-Logic-Reset\n\
  //                  TMS=1      TMS=1           TMS=1           TMS=1\n\
  //out_buffer[num_bytes_to_send++] = 0x4B; //don\'t read data in update-dr->select-dr-scan->select-ir-scan->test-logic-reset\n\
  //out_buffer[num_bytes_to_send++] = 0x03; //no. of clock pulses=length+1(4 clocks here)\n\
  //out_buffer[num_bytes_to_send++] = 0xFF; //data is shifted lsb first, so tms pattern is 1111\n\
  //ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command\n\
  //if (ftdi_status == -666)\n\
  //  printf("USB device unavailable.\\n");\n\
  //else if (ftdi_status < 0)\n\
  //  printf("error code from usb_bulk_write().\\n");\n\
\n\
  //num_bytes_to_send = 0; //reset output buffer\n\
  \n')

#main
if __name__ == '__main__':

  filename = 'auto_demo.c'
  f = open(filename, 'wb')
  generate_main(f)
  ftdi_setup(f)
  reset_chain(f)
  bogus_command(f)
  jtag_setup(f)
  run_test_idle(f)
  irdrscan(f, 0xFF,0xFFFFFFFF)
  dr_exit(f)
  irdrscan(f, 0xFF,0xFFFFFFFF)
  dr_exitl(f)
  ftdi_close(f)
  close_main(f)
  f.close()
