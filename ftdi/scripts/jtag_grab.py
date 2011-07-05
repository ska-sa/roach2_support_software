#!/usr/bin/python
import ftdi
import time

F = ftdi.ftdi_context()

ftdi.ftdi_init(F)

ftdi.ftdi_usb_open(F, 0x0403, 0x6011)

ftdi.ftdi_set_interface(F, ftdi.INTERFACE_D)

ftdi.ftdi_set_bitmode(F, 0x08, ftdi.BITMODE_BITBANG)


ftdi.ftdi_write_data(F, '\x08', 1)

ftdi.ftdi_usb_close(F)
