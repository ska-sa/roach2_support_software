#!/usr/bin/python
import ftdi
import time

F = ftdi.ftdi_context()

ftdi.ftdi_init(F)

ftdi.ftdi_set_interface(F, ftdi.INTERFACE_A)

ftdi.ftdi_usb_open(F, 0x0403, 0x6011)

ftdi.ftdi_set_bitmode(F, 0x00, ftdi.BITMODE_BITBANG)

ftdi.ftdi_usb_close(F)
