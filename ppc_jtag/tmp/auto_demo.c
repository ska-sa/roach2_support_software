#include <stdio.h>
#include <ftdi.h>

#define VENDOR 0x0403
#define PRODUCT 0x6010

void msr(int);
int main(void)
{
  struct ftdi_context ftdi_context; //handle for device
  int ftdi_status = -1; //result of each call

  struct ftdi_device_list *no_devices = 0; //number of devices
  unsigned int dev_index = 0xF; //device in the list used

  unsigned char out_buffer[1024]; //output buffer, commands sent to ft2232h
  int i = 0; //initialze buffer to 0
  for (i = 0; i < 1024; i++)
  {
    out_buffer[i] = 0;
  }
  unsigned char in_buffer[1024]; //input buffer, hold data from ft2232h
  for (i = 0; i < 1024; i++) //initialise buffer to 0
  {
    in_buffer[i] = 0;
  }

  int count = 0; //general loop index
  int num_bytes_to_send = 0; //index for output buffer
  int num_bytes_sent = 0; //count of actual bytes sent - used with write
  int num_bytes_to_read = 0; //number of bytes available to read in drivers input buffer
  int num_bytes_read = 0; //count of actual bytes read - used with read
  int clock_divisor = 0x05DB; //vaulue of clock divisor, scl freq = 60/((1+0x05DB)*2)(MHz)=20KHz

  /*------------------------------------------------------------------------*/
  //does ftdi device exist?
  printf("Checking for FTDI devices...\n");
  ftdi_status = ftdi_usb_find_all(&ftdi_context, &no_devices, VENDOR, PRODUCT);
  if (ftdi_status < 0) //did command execute ok?
  {
    printf("Error in getting number of devices\n");
    return 1;  //exit with error
  }
  if (no_devices < 1) //exit if we dont see any
  {
    printf("There are no FTDI devices installed\n");
    return 1; //exit with error
  }
  printf("%s FTDI devices found - the count includes individual ports on a single chip\n",no_devices);

  /*--------------------------------------------------------------------------
   * Open the port
   *------------------------------------------------------------------------*/

  //initialise a ftdi context
  printf("Initialising FTDI context...\n");
  ftdi_status = ftdi_init(&ftdi_context);
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
    {
      printf("couldn't allocate read buffer\n");
      return 1; //exit with error
    }
    else
    {
      printf("undefined error: %d\n", ftdi_status);
      return 1; //exit with error
    }
  }

  //open ftdi device
  printf("Opening FTDI device...\n");
  ftdi_status = ftdi_usb_open(&ftdi_context, VENDOR, PRODUCT);
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
    {
      printf("Error: %d, usb_find_busses() failed\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -2)
    {
      printf("Error: %d, usb_find_devices() failed\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -3)
    {
      printf("Error: %d, usb device not found\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -4)
    {
      printf("Error: %d, unable to open device\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -5)
    {
      printf("Error; %d, unable to claim device\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -6)
    {
      printf("Error: %d, reset failed\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -7)
    {
      printf("Error: %d, set baudrate failed\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -8)
    {
      printf("Error: %d, get product description failed\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -9)
    {
      printf("Error: %d, get serial number failed\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -10)
    {
      printf("Error: %d, unable to close device\n", ftdi_status);
      return 1;
    }
    else
    {
      printf("Error: %d, undefined error: %d\n", ftdi_status);
      return 1;
    }
  }

  //configure the port parameters
  printf("Configuring port for MPSSE use...\n");
  ftdi_status = ftdi_usb_reset(&ftdi_context);//reset usb
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
    {
      printf("Error: %d, FTDI reset failed\n", ftdi_status);
      return 1;
    }
    else if (ftdi_status == -2)
    {
      printf("Error: %d, USB device unavailable\n", ftdi_status);
      return 1;
    }
    else
    {
      printf("Error: %d, undefined error\n", ftdi_status);
      return 1;
    }
  }

  //set usb transfer sizes to 64k
  ftdi_status = ftdi_write_data_set_chunksize(&ftdi_context, 65536);
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
      printf("Error: %d, ftdi context invalid\n", ftdi_status);
    else
      printf("Error: %d, undefined error\n", ftdi_status);
  }

  //disable event and error characters
  ftdi_status = ftdi_set_event_char(&ftdi_context, 0, 0);
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
      printf("Error: %d, unable to set event character\n", ftdi_status);
    else if (ftdi_status == -2)
      printf("Error: %d, USB device unavailable\n", ftdi_status);
    else
      printf("Error: %d, undefined error\n", ftdi_status);
  }
  ftdi_status = ftdi_set_error_char(&ftdi_context, 0, 0);
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
      printf("Error: %d, unable to set error character\n", ftdi_status);
    else if (ftdi_status == -2)
      printf("Error: %d, USB device unavailable\n", ftdi_status);
    else
      printf("Error: %d, undefined error\n", ftdi_status);
  }

  //set the read and write timouts in milliseconds
  printf("READ AND WRITE TIMEOUTS STILL NEED TO BE SET...\n");

  //set the latency timer to 16ms
  ftdi_status = ftdi_set_latency_timer(&ftdi_context, 16);
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
      printf("Error: %d, latency out of range\n", ftdi_status);
    else if (ftdi_status == -2)
      printf("Error: %d, unable to set latency timer\n", ftdi_status);
    else if (ftdi_status == -3)
      printf("Error: %d, USB device unavailable\n", ftdi_status);
    printf("Error: %d, undefined error\n", ftdi_status);
  }

  //reset controller
  ftdi_status = ftdi_set_bitmode(&ftdi_context, 0x00, BITMODE_RESET);
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
      printf("Error: %d, can't enable bitbang mode\n", ftdi_status);
    else if (ftdi_status == -2)
      printf("Error: %d, USB device unavailable\n", ftdi_status);
    else
      printf("Error, undefined error\n", ftdi_status);
  }

  //enable mpsse mode
  ftdi_status = ftdi_set_bitmode(&ftdi_context, 0x00, BITMODE_MPSSE);
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
      printf("Error: %d, can't enable bitbang mode\n", ftdi_status);
    else if (ftdi_status == -2)
      printf("Error: %d, USB device unavailable\n", ftdi_status);
    else
      printf("Error: %d, undefined error\n", ftdi_status);
  }
  printf("Sleeping for 1.\n");
  sleep(1); //wait for all the usb stuff to complete

  /*------------------------------------------------------------------------*/

  num_bytes_to_send = 0; //zero the index

  out_buffer[num_bytes_to_send++] = 0x4B; //clock data to tms pin(noread)
  out_buffer[num_bytes_to_send++] = 5;
  out_buffer[num_bytes_to_send++] = 0x9F; //tms: 10011111
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);
    //send reset command off
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  num_bytes_to_send = 0; //reset output buffer
  out_buffer[num_bytes_to_send++] = 0xAA; //add bogus command 0xAA to queue
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);
    //send off the bad commands
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  ftdi_status = ftdi_read_data(&ftdi_context, in_buffer, 1024); //read 32 bytes(arb)
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_read().\n");
  else if (ftdi_status == 0)
    printf("no data was available\n");

  num_bytes_to_send = 0; //zero the index

  //set up the high speed specific commands for ft2232h

  out_buffer[num_bytes_to_send++] = 0x8A; //use 60 MHz master clk(disable /5)
  out_buffer[num_bytes_to_send++] = 0x97; //turn off adaptive clocking
  out_buffer[num_bytes_to_send++] = 0x8D; //disable 3 phase clocking

  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send); //send of the high speed commands
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // Set initial states of the MPSSE interface - low byte(lsb), both pin durections and output values
  // Pin name    Signal    Direction    Config    Initial State    Config
  // ADBUS0      TCK       Output       1         low              0
  // ADBUS1      TDI       Output       1         low              0
  // ADBUS2      TDO       Input        0                          0
  // ADBUS3      TMS       Output       1         high?            1
  // ADBUS4      GPIOL0    Input        0                          0
  // ADBUS5      GPIOL1    Input        0                          0
  // ADBUS6      GPIOL2    Input        0                          0
  // ADBUS7      GPIOL3    Input        0                          0

  printf("Setting initial states...\n");
  out_buffer[num_bytes_to_send++] = 0x80; //set data bytes low
  out_buffer[num_bytes_to_send++] = 0x08; //initial state config above(1000)
  out_buffer[num_bytes_to_send++] = 0x0B; //direction config above(1011)

  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off the low GPIO config commands
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");
  num_bytes_to_send = 0; //reset output buffer

  // Set initial states of the MPSSE interface - high byte, both pin directions and output values
  // Pin name    Signal    Direction    Config    Initial State    Config
  // ACBUS0      GPIOH0    Input        0                          0
  // ACBUS1      GPIOH1    Input        0                          0
  // ACBUS2      GPIOH2    Input        0                          0
  // ACBUS3      GPIOH3    Input        0                          0
  // ACBUS4      GPIOH4    Input        0                          0
  // ACBUS5      GPIOH5    Input        0                          0
  // ACBUS6      GPIOH6    Input        0                          0
  // ACBUS7      GPIOH7    Input        0                          0

  out_buffer[num_bytes_to_send++] = 0x82; //set data bytes high
  out_buffer[num_bytes_to_send++] = 0x00; //initial state config above(0000)
  out_buffer[num_bytes_to_send++] = 0x00; //direction config above(0000)

  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off the low GPIO config commands
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  //set TCK frequency
  //TCK = 60MHz/((1+[(1+0xValueH*256) OR 0xValueL])*2)
  out_buffer[num_bytes_to_send++] = '\x86'; //command to set clock divisor
  out_buffer[num_bytes_to_send++] = (clock_divisor & 0xFF);//set 0xValueL of clock divisor
  out_buffer[num_bytes_to_send++] = ((clock_divisor >> 8)& 0xFF);//set 0xValueH of clock divisor
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off the low GPIO config commands
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  //disable internal loopback
  out_buffer[num_bytes_to_send++] = 0x85; //disable loopback
  //loopback is when tdi/do are internally connected for testing

  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off loopback command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer


  // navigate TMS through test-logic-reset->run-test-idle
  //                                        TMS=0
  out_buffer[num_bytes_to_send++] = 0x4B; //dont read data in test-logic-reset, run-test-idle
  out_buffer[num_bytes_to_send++] = 0x00; //number of clock pulses = length+1(1 clock here)
  out_buffer[num_bytes_to_send++] = 0x00; //data is shifted LSB first, so TMS pattern is 0

  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // navigate TMS through run-test-idle->select-DR-scan->select-IR-scan->capture-IR->shift-IR
  //                                     TMS=1           TMS=1           TMS=0       TMS=0
  out_buffer[num_bytes_to_send++] = 0x4B; //dont read data in run-test-idle, select-dr-scan, select-ir-scan
  out_buffer[num_bytes_to_send++] = 0x03; //number of clock pulses = length+1(4 clocks here)
  out_buffer[num_bytes_to_send++] = 0x03; //data is shifted LSB first, so TMS pattern is 1100
                                          //bit 7 is 0 therefore DO/TDI will be 0 for entire duration

  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // TMS is currently 0. State machine is in Shift-IR, so now use the TDI/TDO command to shift data into TDI/DO while reading TDO/DI
  // Although 8 bits shifted in, only need 7 clocks here. The 8th will be in conjunction with the TMS command, coming next

  out_buffer[num_bytes_to_send++] = 0x3B; //clock data out through states Capture-IR, Shift-IR and Exit-IR, read back result
  out_buffer[num_bytes_to_send++] = 0x06; //number of clock pulses = length + 1 (7 clocks here)
  out_buffer[num_bytes_to_send++] = 0xff; //shift out data (ignore last bit)
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // here is the TMS command for 1 clock. Data is also shifted in.

  out_buffer[num_bytes_to_send++] = 0x6B; //clock out TMS, read 1 bit.
  out_buffer[num_bytes_to_send++] = 0x00; //number of pulses = length + 0 (1 here)
  out_buffer[num_bytes_to_send++] = 0x03 & (0xff & 0x80); //11000000&irdi&00000001
  //data is shifted lsb first, so TMS becomes 1, also, bit 7 is shifted into TDI/DO,
  //the 1 in bit 1 will leave TMS high for the next commands.
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  //navigate TMS from Exit-IR through Update-IR->Run-Test-Idle->Select-DR-Scan->Capture-DR->Shift-DR
  //                                  TMS=1      TMS=0          TMS=1           TMS=0       TMS=0

  out_buffer[num_bytes_to_send++] = 0x4B; // don't read data in Update-IR->Run-Test-Idle->Select-DR-Scan->Capture-DR
  out_buffer[num_bytes_to_send++] = 0x04; //no of clock pulses = length+1(5 clks here)
  out_buffer[num_bytes_to_send++] = 0x05; //data is shifted lsb first, so TMS pattern is 10100
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  //navigate TMS from Exit-IR through Update-IR->Select-DR-Scan->Capture-DR->Shift-DR
  //                                  TMS=1      TMS=1           TMS=0       TMS=0
//
  //out_buffer[num_bytes_to_send++] = 0x4B; // don't read data in update-ir->select-dr-scan->capture-dr
  //out_buffer[num_bytes_to_send++] = 0x03; //no of clock pulses = length+1(4 clks here)
  //out_buffer[num_bytes_to_send++] = 0x83; //data is shifted lsb first, so TMS pattern is 1100
  //ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  //if (ftdi_status == -666)
  //  printf("USB device unavailable.\n");
  //else if (ftdi_status < 0)
  //  printf("error code from usb_bulk_write().\n");
//
  //num_bytes_to_send = 0; //reset output buffer

  // TMS is currently low. State Machine is in Shift-DR, so now use the TDI/TDO command to shift drdi out TDI/DO while reading TDO/DI
  // Although 32 bits need shifted in, only 31 are clocked here. The 32nd will be in conjunction with the TMS command. coming next

  out_buffer[num_bytes_to_send++] = 0x3B; //clock data out through states shift-dr and exit-dr
  out_buffer[num_bytes_to_send++] = 0x1E; //no. of clock pulses=length+1(31 clocks here)
  out_buffer[num_bytes_to_send++] = 0xffffffff; //shift out 31bits(ignore last bit)
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  // Here is the TMS command for one clock. Data is also shifted in.

  out_buffer[num_bytes_to_send++] = 0x6B; //clock out tms, read 1 bit
  out_buffer[num_bytes_to_send++] = 0x00; //no. of clock pulses=length+1(1 clocks here)
  out_buffer[num_bytes_to_send++] = 0xC0000000 & (0xffffffff & 0x80000000);
                                         //data is shifted lsb 1st, so tms becomes 1. also, bit 31 is shifted into tdi/do, also a 1
                                         //the 1 in bit 1 will leave tms high for next commands
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // Navigate through Update-DR->Run-Test-Idle->Run-Test-Idle
  //                  TMS=1      TMS=0          TMS=0

  out_buffer[num_bytes_to_send++] = 0x4B; //don't read data in Update-DR->Run-Test-Idle->Run-Test-Idle
  out_buffer[num_bytes_to_send++] = 0x02; //no. of clock pulses=length+1(3 clocks here)
  out_buffer[num_bytes_to_send++] = 0x01; //data is shifted lsb first, so tms pattern is 100
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  ftdi_status = ftdi_read_data(&ftdi_context, in_buffer, 1024); //read 32 bytes(arb)
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_read().\n");
  else if (ftdi_status == 0)
    printf("no data was available\n");

  // navigate TMS through run-test-idle->select-DR-scan->select-IR-scan->capture-IR->shift-IR
  //                                     TMS=1           TMS=1           TMS=0       TMS=0
  out_buffer[num_bytes_to_send++] = 0x4B; //dont read data in run-test-idle, select-dr-scan, select-ir-scan
  out_buffer[num_bytes_to_send++] = 0x03; //number of clock pulses = length+1(4 clocks here)
  out_buffer[num_bytes_to_send++] = 0x03; //data is shifted LSB first, so TMS pattern is 1100
                                          //bit 7 is 0 therefore DO/TDI will be 0 for entire duration

  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // TMS is currently 0. State machine is in Shift-IR, so now use the TDI/TDO command to shift data into TDI/DO while reading TDO/DI
  // Although 8 bits shifted in, only need 7 clocks here. The 8th will be in conjunction with the TMS command, coming next

  out_buffer[num_bytes_to_send++] = 0x3B; //clock data out through states Capture-IR, Shift-IR and Exit-IR, read back result
  out_buffer[num_bytes_to_send++] = 0x06; //number of clock pulses = length + 1 (7 clocks here)
  out_buffer[num_bytes_to_send++] = 0xff; //shift out data (ignore last bit)
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // here is the TMS command for 1 clock. Data is also shifted in.

  out_buffer[num_bytes_to_send++] = 0x6B; //clock out TMS, read 1 bit.
  out_buffer[num_bytes_to_send++] = 0x00; //number of pulses = length + 0 (1 here)
  out_buffer[num_bytes_to_send++] = 0x03 & (0xff & 0x80); //11000000&irdi&00000001
  //data is shifted lsb first, so TMS becomes 1, also, bit 7 is shifted into TDI/DO,
  //the 1 in bit 1 will leave TMS high for the next commands.
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  //navigate TMS from Exit-IR through Update-IR->Run-Test-Idle->Select-DR-Scan->Capture-DR->Shift-DR
  //                                  TMS=1      TMS=0          TMS=1           TMS=0       TMS=0

  out_buffer[num_bytes_to_send++] = 0x4B; // don't read data in Update-IR->Run-Test-Idle->Select-DR-Scan->Capture-DR
  out_buffer[num_bytes_to_send++] = 0x04; //no of clock pulses = length+1(5 clks here)
  out_buffer[num_bytes_to_send++] = 0x05; //data is shifted lsb first, so TMS pattern is 10100
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  //navigate TMS from Exit-IR through Update-IR->Select-DR-Scan->Capture-DR->Shift-DR
  //                                  TMS=1      TMS=1           TMS=0       TMS=0
//
  //out_buffer[num_bytes_to_send++] = 0x4B; // don't read data in update-ir->select-dr-scan->capture-dr
  //out_buffer[num_bytes_to_send++] = 0x03; //no of clock pulses = length+1(4 clks here)
  //out_buffer[num_bytes_to_send++] = 0x83; //data is shifted lsb first, so TMS pattern is 1100
  //ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  //if (ftdi_status == -666)
  //  printf("USB device unavailable.\n");
  //else if (ftdi_status < 0)
  //  printf("error code from usb_bulk_write().\n");
//
  //num_bytes_to_send = 0; //reset output buffer

  // TMS is currently low. State Machine is in Shift-DR, so now use the TDI/TDO command to shift drdi out TDI/DO while reading TDO/DI
  // Although 32 bits need shifted in, only 31 are clocked here. The 32nd will be in conjunction with the TMS command. coming next

  out_buffer[num_bytes_to_send++] = 0x3B; //clock data out through states shift-dr and exit-dr
  out_buffer[num_bytes_to_send++] = 0x1E; //no. of clock pulses=length+1(31 clocks here)
  out_buffer[num_bytes_to_send++] = 0xffffffff; //shift out 31bits(ignore last bit)
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  // Here is the TMS command for one clock. Data is also shifted in.

  out_buffer[num_bytes_to_send++] = 0x6B; //clock out tms, read 1 bit
  out_buffer[num_bytes_to_send++] = 0x00; //no. of clock pulses=length+1(1 clocks here)
  out_buffer[num_bytes_to_send++] = 0xC0000000 & (0xffffffff & 0x80000000);
                                         //data is shifted lsb 1st, so tms becomes 1. also, bit 31 is shifted into tdi/do, also a 1
                                         //the 1 in bit 1 will leave tms high for next commands
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // Navigate from Exit1-DR->Pause-DR->Exit2-DR->Shift-DR
  //                         TMS=0     TMS=1     TMS=0
  out_buffer[num_bytes_to_send++] = 0x4B; //don't read data in Exit1-DR->Pause-DR->Exit2-DR->Shift-DR
  out_buffer[num_bytes_to_send++] = 0x02; //no. of clock pulses=length+1(3 clocks here)
  out_buffer[num_bytes_to_send++] = 0x02; //data is shifted lsb first, so tms pattern is 010
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // Navigate from Shift-DR->Exit1-DR->Update-DR
  //                         TMS=1     TMS=1
  out_buffer[num_bytes_to_send++] = 0x4B; //don't read data in Shift-DR->Exit1-DR->Update-DR
  out_buffer[num_bytes_to_send++] = 0x01; //no. of clock pulses=length+1(2 clocks here)
  out_buffer[num_bytes_to_send++] = 0x83; //data is shifted lsb first, so tms pattern is 11
                                          //the 1 on bit 7 will keep DO/TDI high
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  // Navigate from Update-DR->Run-Test-Idle->Run-Test-Idle
  //                          TMS=0          TMS=0
  out_buffer[num_bytes_to_send++] = 0x4B; //don't read data in Update-DR->Run-Test-Idle->Run-Test-Idle
  out_buffer[num_bytes_to_send++] = 0x01; //no. of clock pulses=length+1(2 clocks here)
  out_buffer[num_bytes_to_send++] = 0x00; //data is shifted lsb first, so tms pattern is 00
                                          //bit 7 is zero->DO/TDI is zero
  ftdi_status = ftdi_write_data(&ftdi_context, out_buffer, num_bytes_to_send);//send off TMS command
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_write().\n");

  num_bytes_to_send = 0; //reset output buffer

  ftdi_status = ftdi_read_data(&ftdi_context, in_buffer, 1024); //read 32 bytes(arb)
  if (ftdi_status == -666)
    printf("USB device unavailable.\n");
  else if (ftdi_status < 0)
    printf("error code from usb_bulk_read().\n");
  else if (ftdi_status == 0)
    printf("no data was available\n");

  /*-------------------------------------------------------------------------
  * Start closing everything down
  *------------------------------------------------------------------------*/

  printf("\nJTAG program executed successfully. \n");
  printf("Press <Enter> to continue\n");
  getchar(); //wait for a carriage return

  //attempt to close ftdi device
  ftdi_status = ftdi_usb_close(&ftdi_context);
  if (ftdi_status != 0)
  {
    if (ftdi_status == -1)
      printf("usb_release failed\n");
    else if (ftdi_status == -2)
      printf("usb_close failed\n");
    else if (ftdi_status == -3)
      printf("ftdi context invalid\n");
    else
      printf("Undefined error: %d\n", ftdi_status);
  }

  //deinitialize a ftdi_context
  ftdi_deinit(&ftdi_context);

  printf("FTDI chip closed and ftdi context deinitialized. \n");
  //printf("Press <Enter> to terminate\n");
  //getchar();
  printf("Goodbye...\n");
  return 0;

}
