### ICANN 2016
#
python3 runExperiment2.py --models "['ModelNSpike',]" --kwmodel "{'model':['spike','cnft'],'nspike':[1,2,3,5,10],'reproductible':False}" --scenarios "['ScenarioControl',]" --nbThread 2 --stats "['StatsTracking1',]" --prefix "NSpike_Control_modelXnspike" --nbThread 8
python3 runExperiment2.py --models "['ModelNSpike',]" --kwmodel "{'model':['spike','cnft'],'nspike':[1,2,3,5,10],'reproductible':False}" --scenarios "['ScenarioControl','ScenarioNoise','ScenarioDistracters','ScenarioTracking']"  --stats "['StatsTracking1',]" --prefix "NSpike_Scenarios_modelXnspike" --nbThread 8

python3 runExperiment2.py --models "['ModelNSpike',]" --kwmodel "{'model':['spike','cnft'],'nspike':[1,2,3,5,10],'reproductible':False}" --scenarios "['ScenarioControl',]"  --stats "['StatsTracking1',]" --prefix "NSpike_Control_modelXnspikeXdt" --nbThread 8 --dt "[0.01,0.05,0.1]"

#compare sequence with prng
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['prng','sequence'],'reproductible':False,'nspike':1,'model':'cnft','clkRatio':80}" --prefix "NSpike_prng_sequence" --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['prng','sequence'],'reproductible':False,'nspike':1,'model':'spike','clkRatio':80}" --prefix "NSpike_prng_sequence_spike"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['prng','sequence'],'reproductible':False,'nspike':1,'model':'spike','clkRatio':80}" --prefix "NSpike_prng_sequence_spike"  --nbThread 8  --scenarios "['ScenarioControl',]"

#compare for differnet nspike
#(for nspike = 20 nbActMax was 17, => dt 438
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['prng','sequence'],'reproductible':False,'nspike':[1,2,3,5,10],'model':'spike','clkRatio':438}" --prefix "NSpike_prng_sequencexnspike_spike"  --nbThread 8  --scenarios "['ScenarioControl',]"

python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['prng','sequence'],'reproductible':False,'nspike':20,'model':'spike','clkRatio':500}" --prefix "NSpike_prng_sequencex20spike_spike"  --nbThread 8  --scenarios "['ScenarioControl',]"

#sequence 1 period = size
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['prng','sequence'],'reproductible':False,'nspike':20,'model':'spike','clkRatio':500}" --prefix "NSpike_prng_sequencexscenario_spike"  --nbThread 8  --scenarios "['ScenarioNoise','ScenarioDistracters','ScenarioTracking']"

#prng spike 10 5 1 for distracters  DONE?
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'prng','reproductible':False,'nspike':10,'model':'spike','clkRatio':378}" --prefix "NSpike_prngxscenario_nspike10"  --nbThread 8  --scenarios "['ScenarioNoise','ScenarioDistracters']"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'prng','reproductible':False,'nspike':5,'model':'spike','clkRatio':238}" --prefix "NSpike_prngxscenario_nspike5"  --nbThread 8  --scenarios "['ScenarioNoise','ScenarioDistracters']" 
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'prng','reproductible':False,'nspike':1,'model':'spike','clkRatio':130}" --prefix "NSpike_prngxscenario_nspike1"  --nbThread 8  --scenarios "['ScenarioNoise','ScenarioDistracters']" 

#seauence 2 period = size*size
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'sequence','reproductible':False,'nspike':20,'model':'spike','clkRatio':500}" --prefix "NSpike_sequencexscenario_spike_period2"  --nbThread 8  --scenarios "['ScenarioNoise','ScenarioDistracters','ScenarioTracking']"
#different spike
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'sequence','reproductible':False,'nspike':[1,2,3,5,10],'model':'spike','clkRatio':500}" --prefix "NSpike_sequencexscenarioxspike_period2"  --nbThread 8  --scenarios "['ScenarioNoise','ScenarioDistracters','ScenarioTracking']"


#rsdnf2  
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf2','reproductible':False,'nspike':1,'model':'spike','clkRatio':80}" --prefix "NSpike_rsdnf2Scenario_1spike"  --nbThread 8  --scenarios "['ScenarioNoise','ScenarioDistracters','ScenarioTracking']"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf2','reproductible':False,'nspike':5,'model':'spike','clkRatio':238}" --prefix "NSpike_rsdnf2Scenario_5spike"  --nbThread 8  --scenarios "['ScenarioNoise','ScenarioDistracters','ScenarioTracking']"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf2','reproductible':False,'nspike':10,'model':'spike','clkRatio':378}" --prefix "NSpike_rsdnf2Scenario_10spike"  --nbThread 3  --scenarios "['ScenarioNoise','ScenarioDistracters','ScenarioTracking']"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf2','reproductible':False,'nspike':20,'model':'spike','clkRatio':500}" --prefix "NSpike_rsdnf2Scenario_20spike"  --nbThread 8  --scenarios "['ScenarioNoise','ScenarioDistracters','ScenarioTracking']"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf2','reproductible':False,'nspike':1,'model':'spike','clkRatio':130}" --prefix "NSpike_rsdnf2control_1spike"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf2','reproductible':False,'nspike':5,'model':'spike','clkRatio':238}" --prefix "NSpike_rsdnf2control_5spike"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf2','reproductible':False,'nspike':10,'model':'spike','clkRatio':378}" --prefix "NSpike_rsdnf2control_10spike"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf2','reproductible':False,'nspike':20,'model':'spike','clkRatio':658}" --prefix "NSpike_rsdnf2control_20spike"  --nbThread 8  --scenarios "['ScenarioControl',]"

#sequence mixte
#base pi = 28
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceMixte','sequenceShortMixte'],'reproductible':False,'nspike':1,'model':'spike','clkRatio':130}" --prefix "NSpike_controle_mixteXshort_nspike1"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceMixte','sequenceShortMixte'],'reproductible':False,'nspike':3,'model':'spike','clkRatio':182}" --prefix "NSpike_controle_mixteXshort_nspike3"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceMixte','sequenceShortMixte'],'reproductible':False,'nspike':5,'model':'spike','clkRatio':238}" --prefix "NSpike_controle_mixteXshort_nspike5"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceMixte','sequenceShortMixte'],'reproductible':False,'nspike':10,'model':'spike','clkRatio':378}" --prefix "NSpike_controle_mixteXshort_nspike10"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceMixte','sequenceShortMixte'],'reproductible':False,'nspike':20,'model':'spike','clkRatio':658}" --prefix "NSpike_controle_mixteXshort_nspike20"  --nbThread 8  --scenarios "['ScenarioControl',]"
#this model is flawed by intra-spike correlation

#sequenceShortMixte version 2 : the propagation direction of the random bits alternate
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceShort','sequenceShortMixte'],'reproductible':False,'nspike':1,'model':'spike','clkRatio':130}" --prefix "NSpike_controle_mixteXshort_nspike1_v2"  --nbThread 3  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceShort','sequenceShortMixte'],'reproductible':False,'nspike':3,'model':'spike','clkRatio':182}" --prefix "NSpike_controle_mixteXshort_nspike3_v2"  --nbThread 3  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceShort','sequenceShortMixte'],'reproductible':False,'nspike':5,'model':'spike','clkRatio':238}" --prefix "NSpike_controle_mixteXshort_nspike5_v2"  --nbThread 3  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceShort','sequenceShortMixte'],'reproductible':False,'nspike':10,'model':'spike','clkRatio':378}" --prefix "NSpike_controle_mixteXshort_nspike10_v2"  --nbThread 3  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'sequenceShortMixte','reproductible':False,'nspike':10,'model':'spike','clkRatio':378}" --prefix "NSpike_controle_mixteXshort_nspike10_v2_part2"  --nbThread 3  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequenceShort','sequenceShortMixte'],'reproductible':False,'nspike':20,'model':'spike','clkRatio':658}" --prefix "NSpike_controle_mixteXshort_nspike20_v2"  --nbThread 8  --scenarios "['ScenarioControl',]"


#sequence vs sequenceMixte version2
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequence','sequenceMixte'],'reproductible':False,'nspike':1,'model':'spike','clkRatio':130}" --prefix "NSpike_controle_mixteXsequence_nspike1"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequence','sequenceMixte'],'reproductible':False,'nspike':5,'model':'spike','clkRatio':238}" --prefix "NSpike_controle_mixteXsequence_nspike5"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequence','sequenceMixte'],'reproductible':False,'nspike':10,'model':'spike','clkRatio':378}" --prefix "NSpike_controle_mixteXsequence_nspike10"  --nbThread 8  --scenarios "['ScenarioControl',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':['sequence','sequenceMixte'],'reproductible':False,'nspike':20,'model':'spike','clkRatio':658}" --prefix "NSpike_controle_mixteXsequence_nspike20"  --nbThread 8  --scenarios "['ScenarioControl',]"

#sequence vs distracters

python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'sequence','reproductible':False,'nspike':1,'model':'spike','clkRatio':130}" --prefix "NSpike_distr_sequence_nspike1"  --nbThread 3  --scenarios "['ScenarioDistracters',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'sequence','reproductible':False,'nspike':5,'model':'spike','clkRatio':238}" --prefix "NSpike_distr_sequence_nspike5"  --nbThread 4  --scenarios "['ScenarioDistracters',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'sequence','reproductible':False,'nspike':10,'model':'spike','clkRatio':378}" --prefix "NSpike_distr_sequence_nspike10"  --nbThread 8  --scenarios "['ScenarioDistracters',]"
python3 runExperiment2.py --models "['ModelNSpike']" --kwmodel "{'cell':'Rsdnf','routerType':'sequence','reproductible':False,'nspike':20,'model':'spike','clkRatio':658}" --prefix "NSpike_distr_sequence_nspike20"  --nbThread 8  --scenarios "['ScenarioDistracters',]"
