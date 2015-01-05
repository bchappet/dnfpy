CC=gcc
CFLAGS=-W -g -Wall -ansi -pedantic
LDFLAGS=
INCDIRS=-I../



libac.so:  array_uchar.o  synchronous_step_moore.o gof_cell.o cell_rsdnf.o synchronous_step_neumann.o cell_transmitters.o
	$(CC) ${INCDIRS} -shared -o $@ $?

%.o: ../%.c
	$(CC) ${INCDIRS} -o $@ -c -fPIC $< $(CFLAGS)


clean:
	rm -rf *.o
