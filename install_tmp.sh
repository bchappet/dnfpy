#!/bin/bash

######To set accordingly##############
DNFPY_HOME=~/Documents/DNFPY/dnfpy
VREP_HOME=~/Documents/bin/V-REP_PRO_EDU_V3_2_1_Linux
ARCHI=32
###################################


export PYTHONPATH=$PYTHONPATH:$DNFPY_HOME/src/
export PYTHONPATH=$PYTHONPATH:$VREP_HOME/programming/remoteApiBindings/python/python/

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DNFPY_HOME/src/dnfpy/cellular/cpp_implementation/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$VREP_HOME/programming/remoteApiBindings/lib/lib/${ARCHI}Bit/
