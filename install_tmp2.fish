#to source
#will add dnfpy and test_dnfpy package to PYTHONPATH
#


#TO SET##
set -x DNFPY_HOME ~/Dropbox/THESE/workspace_python/SDNF/dnfpy
set -x VREP_HOME ~/bin/V-REP_PRO_EDU_V3_2_1_64_Linux
########

set -x -g PYTHONPATH $PYTHONPATH $DNFPY_HOME/src/
set -x -g PYTHONPATH $PYTHONPATH $VREP_HOME/programming/remoteApiBindings/python/python/

set -x -g LD_LIBRARY_PATH $LD_LIBRARY_PATH $DNFPY_HOME/src/dnfpy/cellular/cpp_implementation/
set -x -g LD_LIBRARY_PATH $LD_LIBRARY_PATH $VREP_HOME/programming/remoteApiBindings/lib/lib/64Bit/

