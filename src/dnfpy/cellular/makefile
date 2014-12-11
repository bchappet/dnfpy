CC=gcc
CFLAGS=-W -Wall -ansi -pedantic
LDFLAGS=
EXEC=test

all: $(EXEC)


test: test_array3uint.o array3uint.o
	$(CC) -o $@ $^ $(LDFLAGS)



%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)


clean:
	rm -rf *.o
