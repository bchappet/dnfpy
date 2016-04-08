CC = g++
CFLAGS = -Wall -std=c++11 -g
INCLUDES = ../
SRC_DIR = ../

OBJS = router.o register.o bitstreamutils.o cellrsdnf.o \
	routerSequence.o routerSequenceMixte.o routerBit.o
.SECONDARY : $(OBJS)

all : router_t cellrsdnf_t register_t


%_t : $(OBJS) %_t.cpp  ../module.h
	$(CC) $(CFLAGS) $(OBJS) -I$(INCLUDES) $@.cpp -o $@


%.o : $(SRC_DIR)%.cpp $(SRC_DIR)%.h ../module.h
	$(CC) -c $(CFLAGS) $< -o $@


clean :
	rm *.o *_t

