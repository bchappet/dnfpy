
set paramsWM "'h':-0.02,'tau':0.08,'iExc':2.8,'iInh':1.51,'wExc':0.07,'wInh':0.09,'size':49"
set paramsComp "'h':0.0,'tau':0.138,'iExc':4.393,'iInh':4.268,'wExc':0.379,'wInh':0.623,'size':49,
                'betaSFA':0.2,'tauSFA':0.382,'mSFA':0.102"
#tau forced to 0.5
set spikeWM_tau "'dim': 2, 'wInh': 0.076818989260382456, 'activation': 'step', 'iExc': 2.0419905484839278, 'iInh': 1.4790371433882361, 'size': 49, 'tau': 0.5, 'model': 'spike', 'h': 0.43532126093415568, 'wExc': 0.063832937731023637, 'dt': 0.1, 'lateral': 'dog'"
set spikeComp_tau "'size': 49, 'wExc': 0.20770422544987494, 'wInh': 0.9068255307648978, 'tau': 0.5, 'dt': 0.1, 'iExc': 0.66910641024680828, 'dim': 2, 'iInh': 0.50568635409295715, 'h': 0, 'activation': 'step', 'lateral': 'dog', 'model': 'spike'"

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
#--nbThread 8  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.4,0.6,1.0],'nbDistr':[0,3,5,7,10]}" \
#--timeEnd 40 --prefix "comp_noise_distr"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  \
#--nbThread 4  --scenarios "['WorkingMemoryShift']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.05,0.1,0.15,0.2],'nbDistr':[0,3,5,7,10]}" \
#--timeEnd 40 --prefix "wm_noise_distr"
#
#
#SPIKING DNF

python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$spikeComp}"  \
--nbThread 8  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
--kwscenario "{'noiseI':[0.0,0.4,0.6,1.0],'nbDistr':[0,3,5,7,10]}" \
--timeEnd 40 --prefix "spike_comp_noise_distr"
