CC = gcc
CFLAGS = -fPIC -I/usr/include/python3.12/
LDFLAGS = -L/usr/lib/ -lpython3.12 -ldl -lm
TARGET = holyshell.so
SRC = shell.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) -shared -o $@ $< $(CFLAGS) $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean
