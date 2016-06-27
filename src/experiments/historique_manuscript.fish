#!/usr/bin/fish
set paramsWM "'h':-0.02,'tau':0.08,'iExc':2.8,'iInh':1.51,'wExc':0.07,'wInh':0.09,'size':49"
set paramsComp "'h':0.0,'tau':0.138,'iExc':4.393,'iInh':4.268,'wExc':0.379,'wInh':0.623,'size':49"

set spikeComp1 "'size': 49, 'lateral': 'dog', 'dim': 2, 'dt': 0.1, 'activation': 'step', 'h': 0, 'iInh': 1.2257227318846564, 'wExc': 0.5378432051161548, 'iExc': 1.258482459256403, 'model': 'spike', 'wInh': 1.9637076470086288, 'tau': 0.12769479411269885"
set spikeComp "'model': 'spike', 'dim': 2, 'activation': 'step', 'iInh': 0.64538669980233787, 'tau': 0.12687111199574119, 'size': 49, 'lateral': 'dog', 'h': 0, 'wExc': 0.47008654993640697, 'iExc': 0.6584865701410707, 'dt': 0.1, 'wInh': 0.76977930800179117"

set spikeWM "'h': -0.017157652027138398, 'iInh': 0.23981903558649234, 'size': 49, 'lateral': 'dog', 'wExc': 0.085545540721353147, 'dt': 0.1, 'activation': 'step', 'wrap': False, 'wInh': 0.09819595184879297, 'tau': 0.11709253722498286, 'dim': 2, 'iExc': 0.34302857865247194, 'model': 'spike'"


#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  --nbThread 8  --scenarios "['WorkingMemoryShift']" --kwscenario "{'trackSpeed':[0.0,0.02,0.04,0.06,0.08,0.1]}" --stats "['StatsTracking2']" --timeEnd 40 --prefix "WM_speed"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  --nbThread 8  --scenarios "['WorkingMemoryShift']" --kwscenario "{'noiseI':[0.00,0.02,0.04,0.06,0.08,0.1]}" --stats "['StatsTracking2']" --timeEnd 40 --prefix "WM_noise"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  --nbThread 8  --scenarios "['WorkingMemoryShift']" --kwscenario "{'nbDistr':[0,1,2,3,4,5]}" --stats "['StatsTracking2']" --timeEnd 40 --prefix "WM_distr"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsComp,'sfa':[False,True]}"  \
#--nbThread 8  --scenarios "['ScenarioTracking','ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--timeEnd 40 --prefix "comp_sfa_scenario"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsComp,'tau':[0.1,0.3,0.5,0.7,0.9]}"  \
#--nbThread 8  --scenarios "['ScenarioTracking','ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--timeEnd 40 --prefix "comp_tau_scenario"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsComp}"  \
#--nbThread 8  --scenarios "['ScenarioNoise']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.2,0.4,0.6,0.8,1.0]}" \
#--timeEnd 40 --prefix "comp_noise"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsComp}"  \
#--nbThread 8  --scenarios "['ScenarioDistracters']"  --stats "['StatsTracking2']" \
#--kwscenario "{'nbDistr':[6,7,8,9,10,20,30]}" \
#--timeEnd 40 --prefix "comp_distr_hard"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsComp}"  \
#--nbThread 4  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.4,0.6,1.0],'nbDistr':[0,3,5,7]}" \
#--timeEnd 40 --prefix "comp_noise_distr"

python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  \
--nbThread 4  --scenarios "['WorkingMemoryShift']"  --stats "['StatsTracking2']" \
--kwscenario "{'noiseI':[0.0,0.05,0.1,0.15,0.2],'nbDistr':[0,3,5,7,10]}" \
--timeEnd 40 --prefix "wm_noise_distr"
#
#
#SPIKING DNF

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$spikeComp}"  \
#--nbThread 4  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.4,0.6,1.0],'nbDistr':[0,3,5,7,10]}" \
#--timeEnd 40 --prefix "spike_comp_noise_distr"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$spikeWM}"  \
#--nbThread 8  --scenarios "['WorkingMemoryShift']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.05,0.1,0.15,0.2],'nbDistr':[0,3,5,7,10]}" \
#--timeEnd 40 --prefix "spike_wm_noise_distr"
