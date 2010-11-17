TARGET=auto_demo
CLIBS=-lftdi
CFLAGS=-Wall

$(TARGET): auto_demo.c
	gcc $(CFLAGS) $(CLIBS) -o $@ $^

clean:
	rm -f $(TARGET)
