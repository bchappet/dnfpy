CC = g++
CFLAGS = -Wall -std=c++11 -fPIC -O2 -s
EXEC_NAME = test_lib
INCLUDES =
LIBS =
OBJ_FILES = cellgof.o cellrsdnf.o \
			neuroncasasfast.o \
			register.o map2d.o mooreconnecter.o neumannconnecter.o rsdnfconnecter.o rsdnfconnecter2layer.o \
		   	softsimu.o 	cellsbsfast.o cellsbsfast2.o sbsfastrouter.o bitstream.o bitstreamuint.o \
		   	bitstreamchar.o   cellnspike.o nspikeconnecter.o  cellbsrsdnf.o bsrouter.o carrybsrouter.o \
		   	bitstreamutils.o router.o param.o routerSequence.o \
			routerSequenceMixte.o \
			sequenceConnecter.o \
			cellrsdnf2.o \
			routerBit.o \
			bitstreamfloat.o  bitstreamfloatgenerator.o cellsbsfloat.o sbsfloatrouter.o \

INSTALL_DIR = /usr/bin

test : $(EXEC_NAME)

lib : $(OBJ_FILES)
	$(CC)  -o libhardsimu.so $? -shared

clean :
	  rm $(EXEC_NAME) $(OBJ_FILES)

$(EXEC_NAME) : $(OBJ_FILES) main.o
	  $(CC) $(CFLAGS) -o $(EXEC_NAME) $? $(LIBS)

%.o: %.cpp
	  $(CC) $(CFLAGS) $(INCLUDES) -o $@ -c $<

%.o: %.cc
	  $(CC) $(CFLAGS) $(INCLUDES) -o $@ -c $<

%.o: %.c
	  gcc $(CFLAGS) $(INCLUDES) -o $@ -c $<

install :
	  cp $(EXEC_NAME) $(INSTALL_DIR)
