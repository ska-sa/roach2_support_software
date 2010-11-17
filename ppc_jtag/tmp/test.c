#include <stdio.h>

int main(void)
{
  int ftdi_status = 0;

  while (ftdi_status != -11)
    {
      if (ftdi_status != 0)
      {
        if (ftdi_status == -1)
        {
          printf("Error: %d, usb_find_busses() failed\n", ftdi_status);
          //return 1;
        }
        else if (ftdi_status == -2)
        {
          printf("Error: %d, usb_find_devices() failed\n", ftdi_status);
          //return 1;
        }
        else if (ftdi_status == -3)
        {
          printf("Error: %d, usb device not found\n", ftdi_status);
          //return 1;
        }
        else if (ftdi_status == -4)
        {
          printf("Error: %d, unable to open device\n", ftdi_status);
          //return 1;
        }
        else if (ftdi_status == -5)
        {
          printf("Error; %d, unable to claim device\n", ftdi_status);
          //return 1;
        }
        else if (ftdi_status == -6)
        {
          printf("Error: %d, reset failed\n", ftdi_status);
          //return 1;
        }
        else if (ftdi_status == -7)
        {
          printf("Error: %d, set baudrate failed\n", ftdi_status);
          //return 1;
        }
        else if (ftdi_status == -8)
        {
          printf("Error: %d, get product description failed\n", ftdi_status);
          //return 1;
        }
        else if (ftdi_status == -9)
        {
          printf("Error: %d, get serial number failed\n", ftdi_status);
          //return 1;
        }
        else if (ftdi_status == -10)
        {
          printf("Error: %d, unable to close device\n", ftdi_status);
          //return 1;
        }
        else
        {
          printf("Error: %d, undefined error: %d\n", ftdi_status);
          //return 1;
        }
      }
      ftdi_status--;
    }
}
