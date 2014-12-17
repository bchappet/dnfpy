CC=gcc
CFLAGS=-W -g -Wall -ansi -pedantic
LDFLAGS=
INCDIRS=-I../



libac.so: cellular_computation.o array_uchar.o cell_computation.o
	$(CC) ${INCDIRS} -shared -o $@ $?

%.o: ../%.c
	$(CC) ${INCDIRS} -o $@ -c -fPIC $< $(CFLAGS)


clean:
	rm -rf *.o
