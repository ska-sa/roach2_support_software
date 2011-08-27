/*

this program attempts to send I2C stuff over the FTDI interface but fails

*/

#include <stdio.h>
#include <unistd.h>
#include <ftdi.h>

#define IIC_CMD_RD 0x80
#define IIC_CMD_WR 0x00

struct ftiic_data {
	struct ftdi_context* ftdic;
	/* IIC clock frequency in Hz */
	unsigned int freq;
	/* store the current sda and scl values */
	unsigned char sda;
	unsigned char scl;
};

/*
int i2c_send_start(struct ftdi_context *fc)
{
	int ret;
	unsigned char wdata[WSIZE] = {SET_BITS_LOW, 0x0, 0x3,
	                              SET_BITS_HIGH, 0x0, 0x0,
		                      TCK_DIVISOR, 0x4, 0x0,
	                              LOOPBACK_END,
				      RDWR, 0x3, 0x0, 0x12, 0x34, 0x56,
				      SEND_IMMEDIATE};
	unsigned char rdata[RSIZE];
	
	ret = ftdi_write_data(fc, wdata, WSIZE);
	if (ret < 0) {
		fprintf(stderr, "write error: %s\n", 
						ftdi_get_error_string(fc));
		return -1;
	} else if (ret < WSIZE) {
		fprintf(stderr, "write error: wrote %d bytes, expected %d\n", 
						ret, WSIZE);
		return -1;
	}
	ret = ftdi_read_data(fc, rdata, RSIZE);
	if (ret < 0) {
		fprintf(stderr, "read error: %s\n", 
						ftdi_get_error_string(fc));
		return -1;
	} else if (ret < RSIZE) {
		fprintf(stderr, "warning : read %d bytes, expected %d\n", 
						ret, RSIZE);
	}
	{
		int i;
		for (i=0; i < RSIZE; i++) {
			printf("%2d - 0x%02x \n", i, rdata[i]);
		}
	}
	return 0;
}
*/

void dump_pins(struct ftiic_data* iic_data, int n){
	struct ftdi_context *fc = iic_data->ftdic;
	unsigned char debug;
	//ftdi_read_pins(fc, &debug);
	//printf("dump[%d] pins = %x\n", n, debug);
}


static void iic_readfok(struct ftiic_data* iic_data)
{
	struct ftdi_context *fc = iic_data->ftdic;
	unsigned char debug[128];
	int ret;
	ret = ftdi_read_data(fc, debug, 128);
	if (ret < 0) {
		fprintf(stderr, "read error: %s\n", 
				ftdi_get_error_string(fc));
	} else {
		printf("fok ack read = %x, next = %x, rcv = %x\n",
				debug[0], debug[1], ret);
	}
}



int iic_set_bits (struct ftiic_data* iic_data, unsigned char scl_val,
					       unsigned char sda_val,
					       unsigned char scl_dir,
					       unsigned char sda_dir,
					       unsigned char sync) {
	struct ftdi_context *fc = iic_data->ftdic;
	unsigned char data[4] = {SET_BITS_LOW, 0x0, 0x0, SEND_IMMEDIATE};
	int ret;

	data[2] = (scl_dir ? 0x1 : 0x0) | (sda_dir ? 0x2 : 0x0);
	data[1] = (scl_val ? 0x1 : 0x0) | (sda_val ? 0x2 : 0x0);
	ret = ftdi_write_data(fc, data, sync ? 4 : 3);
	if (ret < 0) {
		fprintf(stderr, "write error: %s\n", 
						ftdi_get_error_string(fc));
		return -1;
	} else if (ret < (sync ? 4 : 3)) {
		fprintf(stderr, "write error: wrote %d bytes, expected %d\n", 
						ret, sync ? 4 : 3);
		return -1;
	}
	iic_data->sda = sda_val;
	iic_data->scl = scl_val;
	/* if sync, make sure you delay one cycle after */
	if (sync && iic_data->freq < 1000000)
		usleep(1000000/iic_data->freq);

	//printf("sda == %d, scl == %d ? ", sda_dir, scl_dir);
	dump_pins(iic_data, 0);
	return 0;
}

int iic_send_start(struct ftiic_data* iic_data) {
	int ret;
	/* TODO: add start == '0' check */

	/* prepare for start bit condition: scl = 1 and sda 1 -> 0 */
	if (iic_data->scl == 0) {
		if (iic_data->sda == 0) {
			ret = iic_set_bits(iic_data, 0, 1, 1, 1, 1);
			if (ret)
				return ret;
		}
		ret = iic_set_bits(iic_data, 1, 1, 1, 1, 1);
		if (ret)
			return ret;
	} else {
		if (iic_data->sda == 0) {
			ret = iic_set_bits(iic_data, 0, 0, 1, 1, 1);
			if (ret)
				return ret;
			ret = iic_set_bits(iic_data, 0, 1, 1, 1, 1);
			if (ret)
				return ret;
			ret = iic_set_bits(iic_data, 1, 1, 1, 1, 1);
			if (ret)
				return ret;
		}
	}
	/* issue start bit */
	ret = iic_set_bits(iic_data, 1, 0, 1, 1, 1);
	if (ret)
		return ret;
	return 0;
}

int iic_send_stop(struct ftiic_data* iic_data) {
	int ret;
	/* prepare for start bit condition: scl = 1 and sda 1 -> 0 */
	if (iic_data->scl == 0) {
		if (iic_data->sda == 1) {
			ret = iic_set_bits(iic_data, 0, 0, 1, 1, 1);
			if (ret)
				return ret;
		}
		ret = iic_set_bits(iic_data, 1, 0, 1, 1, 1);
		if (ret)
			return ret;
	} else {
		if (iic_data->sda == 1) {
			ret = iic_set_bits(iic_data, 0, 1, 1, 1, 1);
			if (ret)
				return ret;
			ret = iic_set_bits(iic_data, 0, 0, 1, 1, 1);
			if (ret)
				return ret;
			ret = iic_set_bits(iic_data, 1, 0, 1, 1, 1);
			if (ret)
				return ret;
		}
	}
	/* issue start bit */
	ret = iic_set_bits(iic_data, 1, 0, 1, 1, 1);
	if (ret)
		return ret;

	return 0;
}

int iic_write_byte(struct ftiic_data* iic_data, unsigned char val){
	struct ftdi_context *fc = iic_data->ftdic;
	unsigned char data[4];
	int ret;
	printf ("writing byte %x\n",val);
	data[0] = MPSSE_DO_WRITE | MPSSE_LSB | MPSSE_WRITE_NEG;
	data[1] = 0x0;
	data[2] = 0x0;
	data[3] = val;
	ret = ftdi_write_data(fc, data, 4);
	if (ret < 0) {
		fprintf(stderr, "write error: %s\n", 
						ftdi_get_error_string(fc));
		return -1;
	}
	iic_data->sda = (val & 0x80) >> 8;

	/* TODO: is this right */
	iic_data->scl = 0;
	return 0;
}

int iic_check_ack(struct ftiic_data* iic_data, unsigned char *ack,
						unsigned char sda_input){
	struct ftdi_context *fc = iic_data->ftdic;

	unsigned char debug[128];

	unsigned char data[6];
	int ret = 0;
	int failed = 0;
	data[0] = SET_BITS_LOW;
	data[1] = ((iic_data->sda & 0x1) << 1) | ((iic_data->scl & 0x1));
	data[2] = 0x1; /* set sda to input */
	data[3] = MPSSE_DO_WRITE | MPSSE_DO_READ | MPSSE_LSB |
		                    MPSSE_WRITE_NEG | MPSSE_BITMODE;
	data[4] = 0x1; /* only 1 bit */
	data[5] = 0x1;

	failed = 1;
	dump_pins(iic_data, 666);
	ret = ftdi_write_data(fc, data, 6);
	dump_pins(iic_data, 666);
	if (ret < 0) {
		fprintf(stderr, "write error: %s\n", 
						ftdi_get_error_string(fc));
	} else if (ret != 6)  {
		fprintf(stderr, "write error: wrote %d bytes, expected %d\n",
							ret, 6);
	} else {
		ret = ftdi_read_data(fc, debug, 128);
		if (ret < 0) {
			fprintf(stderr, "read error: %s\n", 
					ftdi_get_error_string(fc));
		} else if (ret != 1)  {
  			fprintf(stderr, "read error: read %d bytes,\
  						expected %d", ret, 1); 
		} else {
			failed = 0;
			*ack = debug[0];
			ftdi_read_pins(fc, debug);
			printf("read ack = %x (pins = %x)\n", *ack,debug[0]);
		}
	}
	if (!sda_input) {
		/* set sda back to output */
		data[2] = 0x3; 
		ret = ftdi_write_data(fc, data, 3);
		if (ret < 0) {
			fprintf(stderr, "write error: %s\n", 
					ftdi_get_error_string(fc));
			failed = 1;
		} else if (ret != 3) {
			fprintf(stderr, "write error: wrote %d bytes, \
					expected %d\n", ret, 3);
			failed = 1;
		}
	}

	return (failed) ? -1 : 0;
}

static int ftiic_probe_dev(struct ftiic_data* iic_data, unsigned char addr)
{
	unsigned char ack = 0;

	dump_pins(iic_data, 0);
	if (iic_send_start(iic_data)) {
		fprintf(stderr, "probe dev failed: send start failed\n");
		return -1;
	}

	dump_pins(iic_data, 1);
	if (iic_write_byte(iic_data, (addr & 0x7f) | IIC_CMD_RD)) {
		fprintf(stderr, "probe dev failed: send stop failed\n");
		return -1;
	}

	dump_pins(iic_data, 2);
	if (iic_check_ack(iic_data, &ack, 0)){
		fprintf(stderr, "probe dev failed: read ack failed\n");
		return -1;
	}

	dump_pins(iic_data, 3);
	if (iic_send_stop(iic_data)) {
		fprintf(stderr, "probe dev failed: send stop failed\n");
		return -1;
	}

	return ack;
}

static int ftiic_setclock(struct ftiic_data* iic_data, unsigned int freq)
{
	struct ftdi_context *fc = iic_data->ftdic;
	int divisor = 6e6 / freq;
	unsigned char data[3] = {TCK_DIVISOR, divisor, 0x0};
	int ret;
	printf("divisor %d\n", divisor);

	iic_data->freq = freq;

	ret = ftdi_write_data(fc, data, 3);
	if (ret < 0) {
		fprintf(stderr, "write error: %s\n", 
						ftdi_get_error_string(fc));
		return -1;
	} else if (ret < 3) {
		fprintf(stderr, "write error: wrote %d bytes, expected %d\n", 
						ret, 3);
		return -1;
	}
	return 0;

}

static void ftiic_destroy(struct ftiic_data* iic_data)
{
	ftdi_usb_close (iic_data->ftdic);
	ftdi_deinit (iic_data->ftdic);
}

static int ftiic_init(struct ftiic_data* iic_data,
		      unsigned int usb_vid,
		      unsigned int usb_pid,
		      unsigned int interface,
		      char* usb_serialno)
{
	struct ftdi_context *fc = iic_data->ftdic;
	int ret;
	unsigned char junk_data [1024];

	if (ftdi_init(fc) < 0) {
		fprintf(stderr, "ftdi_init failed\n");
		return EXIT_FAILURE;
	}
	/* TODO: add serial number check */
	ret = ftdi_usb_open(fc, usb_vid, usb_pid);
	if (ret < 0) {
		fprintf(stderr, "unable to open ftdi device: %s\n",
				ftdi_get_error_string(fc));
		ftdi_deinit (fc);
		return -1;
	}
	ret = ftdi_set_interface(fc, interface);
	if (ret < 0) {
		fprintf(stderr, "unable to set ftdi interface: %s\n",
				ftdi_get_error_string(fc));
		ftiic_destroy(iic_data);
		return -1;
	}
	ret = ftdi_set_latency_timer(fc, 16);
	if (ret < 0) {
		fprintf(stderr, "unable to set ftdi latency: %s\n",
				ftdi_get_error_string(fc));
		return -1;
		ftiic_destroy(iic_data);
	}
	ret = ftdi_usb_reset (fc);
	if (ret < 0) {
		fprintf(stderr, "ftdi reset failed: %s",
				ftdi_get_error_string (fc));
		return -1;
		ftiic_destroy(iic_data);
	}
	ret = ftdi_usb_purge_buffers (fc);
	if (ret < 0) {
		fprintf(stderr, "ftdi purge buffers failed: %s",
				ftdi_get_error_string (fc));
		ftiic_destroy(iic_data);
		return -1;
	}
	ret = ftdi_usb_purge_rx_buffer (fc);
	if (ret < 0) {
		fprintf(stderr, "ftdi purge rx buffer failed: %s",
				ftdi_get_error_string (fc));
		ftiic_destroy(iic_data);
		return -1;
	}
	ret = ftdi_usb_purge_tx_buffer (fc);
	if (ret < 0) {
		fprintf(stderr, "ftdi purge tx buffer failed: %s",
				ftdi_get_error_string (fc));
		ftiic_destroy(iic_data);
		return -1;
	}
	/* We read whatever junk is left over from previous activity
	   I am confused as to why this isn't sorted by flushing */
	do {
		ret = ftdi_read_data (fc, junk_data, 1024);
		if (ret < 0) {
			fprintf(stderr, "ftdi init read failed: %s",
					ftdi_get_error_string (fc));
			ftiic_destroy(iic_data);
			return -1;
		}
	} while (ret > 0);
	/* set sda and scl writable */
	ret = ftdi_set_bitmode(fc, 0x3, BITMODE_MPSSE);
	if (ret < 0) {
		fprintf(stderr, "ftdi set bitmode failed: %s",
				ftdi_get_error_string (fc));
		ftiic_destroy(iic_data);
		return -1;
	}
	/* check that sda/scl are not being driven */
	ret = iic_set_bits(iic_data, 1, 1, 0, 0, 1);
	if (ret < 0) {
		fprintf(stderr, "write error: %s\n", 
						ftdi_get_error_string(fc));
	}
	//dump_pins(iic_data, 128);

	/* set the initial sda/scl values */
	ret = iic_set_bits(iic_data, 1, 1, 1, 1, 1);
	if (ret < 0) {
		fprintf(stderr, "write error: %s\n", 
						ftdi_get_error_string(fc));
	}

	return 0;
}


int main(int argc, char **argv)
{
	struct ftdi_context ftdic;
	struct ftiic_data iic_data;
	int ret;
	unsigned char i;

	iic_data.ftdic = &ftdic;

	if (ftiic_init(&iic_data, 0x403, 0x6011, INTERFACE_B, "") < 0) {
		return -1;
	}
	if (ftiic_setclock(&iic_data, 100000)) {
		fprintf(stderr, "warning: failed to set clock rate\n");
	}

	for (i=0; i < 128; i++){
		//i = 0x53;
		ret = ftiic_probe_dev(&iic_data, i);
		if (ret < 0) {
			fprintf(stderr, "error when issuing probe\n");
			//break;
		} else if (ret == 0) {
			printf("found device at %x\n", i);
		} else {
			printf("no device at %x\n", i);
		}

		/*
		i = 0x41;
		
		ret = ftiic_probe_dev(&iic_data, i);
		if (ret < 0) {
			fprintf(stderr, "error when issuing probe\n");
			//break;
		} else if (ret == 0) {
			printf("found device at %x\n", i);
		} else {
			printf("no device at %x\n", i);
		}
		*/
	}

	ftiic_destroy(&iic_data);

	return 0;
}
