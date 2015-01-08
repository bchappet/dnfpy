CC = g++
CFLAGS = -Wall -std=c++11 -fPIC -O2 -s
EXEC_NAME = test_lib
INCLUDES =
LIBS =
OBJ_FILES = cellgof.o cellrsdnf.o register.o map2d.o mooreconnecter.o neumannconnecter.o rsdnfconnecter.o softsimu.o  cellnspike.o nspikeconnecter.o router.o param.o

INSTALL_DIR = /usr/bin

test : $(EXEC_NAME)

lib : $(OBJ_FILES)
	$(CC)  -o libhardsimu.so $? -shared

clean :
	  rm $(EXEC_NAME) $(OBJ_FILES)

$(EXEC_NAME) : $(OBJ_FILES) main.o
	  $(CC) -o $(EXEC_NAME) $? $(LIBS)

%.o: %.cpp
	  $(CC) $(CFLAGS) $(INCLUDES) -o $@ -c $<

%.o: %.cc
	  $(CC) $(CFLAGS) $(INCLUDES) -o $@ -c $<

%.o: %.c
	  gcc $(CFLAGS) $(INCLUDES) -o $@ -c $<

install :
	  cp $(EXEC_NAME) $(INSTALL_DIR)
