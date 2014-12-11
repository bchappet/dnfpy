CC=gcc
CFLAGS=-W -g -Wall -ansi -pedantic
LDFLAGS=
EXEC=test

all: $(EXEC)


test: test_array_uint.o array_uint.o
	$(CC) -o $@ $^ $(LDFLAGS)



%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)


clean:
	rm -rf *.o
