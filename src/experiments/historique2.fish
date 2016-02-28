### ICANN 2016
#
python3 runExperiment2.py --models "['ModelNSpike',]" --kwmodel "{'model':['spike','cnft'],'nspike':[1,2,3,5,10],'reproductible':False}" --scenarios "['ScenarioControl',]" --nbThread 2 --stats "['StatsTracking1',]" --prefix "NSpike_Control_modelXnspike" --nbThread 8
python3 runExperiment2.py --models "['ModelNSpike',]" --kwmodel "{'model':['spike','cnft'],'nspike':[1,2,3,5,10],'reproductible':False}" --scenarios "['ScenarioControl','ScenarioNoise','ScenarioDistracters','ScenarioTracking']"  --stats "['StatsTracking1',]" --prefix "NSpike_Scenarios_modelXnspike" --nbThread 8

python3 runExperiment2.py --models "['ModelNSpike',]" --kwmodel "{'model':['spike','cnft'],'nspike':[1,2,3,5,10],'reproductible':False}" --scenarios "['ScenarioControl',]"  --stats "['StatsTracking1',]" --prefix "NSpike_Control_modelXnspikeXdt" --nbThread 8 --dt "[0.01,0.05,0.1]"
