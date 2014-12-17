CC=gcc
CFLAGS=-W -g -Wall -ansi -pedantic
LDFLAGS=
EXEC=test test_ca

all: $(EXEC)


test_ca: test_cellular_computation.o array_uchar.o cellular_computation.o cell_computation.o
	$(CC) -o $@ $^ $(LDFLAGS)

test: test_array_uchar.o array_uchar.o cell_computation.o
	$(CC) -o $@ $^ $(LDFLAGS)



%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)


clean:
	rm -rf *.o
