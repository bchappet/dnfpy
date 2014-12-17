CC=gcc
CFLAGS=-W -g -Wall -ansi -pedantic
LDFLAGS=
INCDIRS=-I../



libac.so:  array_uchar.o cell_computation.o synchronous_step.o
	$(CC) ${INCDIRS} -shared -o $@ $?

%.o: ../%.c
	$(CC) ${INCDIRS} -o $@ -c -fPIC $< $(CFLAGS)


clean:
	rm -rf *.o
