CC = g++
CFLAGS = -Wall -std=c++11 -g
INCLUDES = ../
SRC_DIR = ../

OBJS = test_utils.o router.o register.o bitstreamutils.o cellrsdnf.o \
	routerSequence.o routerSequenceMixte.o routerBit.o \
	map2d.o rsdnfconnecter.o neumannconnecter.o \
	cellbsrsdnf.o bsrouter.o carrybsrouter.o \
	bitstreamuint.o bitstream.o neuroncasasfast.o sbsfastrouter.o \
	rsdnfconnecter2layer.o  cellrsdnf2.o
.SECONDARY : $(OBJS) 

all : router_t cellrsdnf_t register_t module_t map2d_t bsRsdnfMap_t bitstreamuint_t neuroncasasfast_t \
	neuroncasasfastMap_t cellbsrsdnf_t rsdnf2layer_map_t 

test : router_t cellrsdnf_t register_t module_t map2d_t bsRsdnfMap_t bitstreamuint_t neuroncasasfast_t \
	neuroncasasfastMap_t cellbsrsdnf_t rsdnf2layer_map_t
	./router_t & ./cellrsdnf_t & ./register_t & ./module_t & ./map2d_t & ./bsRsdnfMap_t & ./bitstreamuint_t & ./neuroncasasfast_t & ./neuroncasasfastMap_t & ./cellbsrsdnf_t & ./rsdnf2layer_map_t



%_t : $(OBJS) %_t.cpp  ../module.h
	$(CC) $(CFLAGS) $(OBJS) -I$(INCLUDES) $@.cpp -o $@

test_utils.o : test_utils.cpp
	$(CC) -c $(CFLAGS) $< -o $@

%.o : $(SRC_DIR)%.cpp $(SRC_DIR)%.h ../module.h
	$(CC) -c $(CFLAGS) $< -o $@


clean :
	rm *.o *_t

