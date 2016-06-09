
set paramsWM "'h':-0.02,'tau':0.08,'iExc':2.8,'iInh':1.51,'wExc':0.07,'wInh':0.09,'size':49,'reproductible':False"

#python3 main.py --params "{$paramsWM}" --scenario WorkingMemoryShift
#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  --nbThread 8  --scenarios "['WorkingMemoryShift']" --kwscenario "{'trackSpeed':[0.0,0.02,0.04,0.06,0.08,0.1]}" --stats "['StatsTracking2']" --timeEnd 40 --prefix "WM_speed"

python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  --nbThread 8  --scenarios "['WorkingMemoryShift']" --kwscenario "{'noiseI':[0.0,0.2,0.4,0.6,0.8,1.0]}" --stats "['StatsTracking2']" --timeEnd 40 --prefix "WM_bignoise"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  --nbThread 8  --scenarios "['ScenarioTracking','ScenarioRobustness']"
#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{}" --prefix "DNFSPFA_tracking"  --nbThread 8  --scenarios "['ScenarioTracking','ScenarioRobustness']"
