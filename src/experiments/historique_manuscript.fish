#!/usr/bin/fish
#set paramsWM "'h':-0.02,'tau':0.08,'iExc':2.8,'iInh':1.51,'wExc':0.07,'wInh':0.09,'size':49"
set paramsWM "'activation': 'sigm', 'beta': 14.906133218303598, 'dt': 0.1, 'lateral': 'dog', 'wrap': False, 'wInh': 0.11361666606738127, 'iInh': 2.3072328003415472, 'model': 'cnft', 'dim': 2, 'size': 49, 'wExc': 0.080912167102385191, 'tau': 0.066010885708270059, 'h': -0.29140668774489337, 'iExc': 4.0424277492796516"

set paramsComp "'h':0.0,'tau':0.138,'iExc':4.393,'iInh':4.268,'wExc':0.379,'wInh':0.623,'size':49"

set spikeComp "'model': 'spike', 'dim': 2, 'activation': 'step', 'iInh': 0.64538669980233787, 'tau': 0.12687111199574119, 'size': 49, 'lateral': 'dog', 'h': 0, 'wExc': 0.47008654993640697, 'iExc': 0.6584865701410707, 'dt': 0.1, 'wInh': 0.76977930800179117"

set spikeWM "'h': -0.017157652027138398, 'iInh': 0.23981903558649234, 'size': 49, 'lateral': 'dog', 'wExc': 0.085545540721353147, 'dt': 0.1, 'activation': 'step', 'wrap': False, 'wInh': 0.09819595184879297, 'tau': 0.11709253722498286, 'dim': 2, 'iExc': 0.34302857865247194, 'model': 'spike'"

set doeComp "'activation': 'step', 'wInh': 0.42349918174573897, 'size': 49, 'lateral': 'doe', 'dim': 2, 'iExc': 0.45966561005045875, 'dt': 0.1, 'tau': 0.12452915458052416, 'wExc': 0.11064375112902931, 'h': 0, 'model': 'spike', 'iInh': 0.41112713239240262"

set doeWM "'tau': 0.14063256668214399, 'wrap': False, 'wInh': 8.9475694220854379e-05, 'h': -0.007487061085547933, 'lateral': 'doe', 'activation': 'step', 'dt': 0.1, 'iInh': 0.58917091389618548, 'model': 'spike', 'size': 49, 'dim': 2, 'iExc': 0.7892948121825627, 'wExc': 1.1180751779961808e-05"


set doeCnftComp "'activation': 'step', 'dim': 2, 'tau': 0.35, 'wExc': 0.13645725851230159, 'wInh': 0.93385423894384245, 'iExc': 2.4047890164818435, 'dt': 0.1, 'lateral': 'doe', 'h': 0, 'size': 49, 'wrap': True, 'model': 'cnft', 'iInh': 2.1123543371374418"

set doeCnftWM "'wInh': 0.00033447307388512416, 'iInh': 8.3605780320093235, 'model': 'cnft', 'iExc': 9.6847892915534928, 'dim': 2, 'h': -0.046522162244893007, 'wrap': False, 'size': 49, 'wExc': 0.00012799533528612018, 'lateral': 'doe', 'activation': 'step', 'dt': 0.1, 'tau': 0.051016909478305256"


set casasComp "'lateral': 'doe', 'wExc': 1.0000000000000001e-05, 'wInh': 1.0, 'dim': 2, 'activation': 'step', 'wrap': True, 'dt': 0.1, 'iInh': 0.068514147151743671, 'size': 49, 'iExc': 0.15764664291031305, 'model': 'spike', 'h': 0.0, 'sizeStream':1500,'pSpike':0.01,'tau':0.12"


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

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  \
#--nbThread 4  --scenarios "['WorkingMemoryShift']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.05,0.1,0.2],'nbDistr':[0,3,5,7]}" \
#--timeEnd 40 --prefix "wm_noise_distr"
#
#
#SPIKING DNF

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$spikeComp}"  \
#--nbThread 4  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.4,0.6,1.0],'nbDistr':[0,3,5,7]}" \
#--timeEnd 40 --prefix "spike_comp_noise_distr"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$spikeWM}"  \
#--nbThread 8  --scenarios "['WorkingMemoryShift']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.05,0.1,0.2],'nbDistr':[0,3,5,7]}" \
#--timeEnd 40 --prefix "spike_wm_noise_distr"

#Spiking DOE
#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$doeComp}"  \
#--nbThread 4  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.4,0.6,1.0],'nbDistr':[0,3,5,7]}" \
#--timeEnd 40 --prefix "doe_comp_noise_distr"

#recompute new scenario WmCluster
#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$paramsWM}"  \
#--nbThread 8  --scenarios "['WmCluster']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.05,0.1,0.2],'nbDistr':[0,3,5,7]}" \
#--timeEnd 40 --prefix "cnft_wm2_noise_distr"


#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$spikeWM}"  \
#--nbThread 8  --scenarios "['WmCluster']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.05,0.1,0.2],'nbDistr':[0,3,5,7]}" \
#--timeEnd 40 --prefix "spike_wm2_noise_distr"

#python3 runExperiment2.py --models "['ModelDNF']" --kwmodel "{$doeWM}"  \
#--nbThread 8  --scenarios "['WmCluster']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.05,0.1,0.2],'nbDistr':[0,3,5,7]}" \
#--timeEnd 40 --prefix "doe_wm2_noise_distr"

#python3 runExperiment2.py --models "['ModelNSpike']" \
#--kwmodel "{$doeWM,'nspike':[10,20,30,40,50,100,150,200,500,1000]}"  \
#--nbThread 8  --scenarios "['WmCluster']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.1,'nbDistr':3}" \
#--timeEnd 40 --prefix "nspike_wm2_nspike_noise1distr3"



#python3 runExperiment2.py --models "['ModelNSpike']" \
#--kwmodel "{$doeWM,'nspike':[500,1000,2000,5000]}"  \
#--nbThread 8  --scenarios "['WmCluster']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.01,'nbDistr':0}" \
#--timeEnd 40 --prefix "nspike_wm2_nspike"


#python3 runExperiment2.py --models "['ModelNSpike']" \
#--kwmodel "{$doeComp,'nspike':[1,2,3,4,6,8,10,12,14,16,18,20,30,40,50]}"  \
#--nbThread 8  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.4,'nbDistr':5}" \
#--timeEnd 40 --prefix "nspike_comp_nspike"
#
#
##CASAS


#python3 runExperiment2.py --models "['ModelBsRsdnf']" \
#--kwmodel "{$doeComp,'sizeStream':[100,500,1000,1500,2000,5000]}"  \
#--nbThread 8  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.4,'nbDistr':5}" \
#--timeEnd 40 --prefix "casas_comp_sizestream"
#
#Check param theoric
#delta found with science!
#

#python3 runExperiment2.py --models "['ModelBsRsdnf']" \
#--kwmodel "{$doeComp,'sizeStream':[500,600,700,1000],'delta':0.00125}"  \
#--nbThread 8  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.4,'nbDistr':3}" \
#--timeEnd 40 --prefix "casas_test_comp_delta_sizestream1"

#Test robustes
#python3 runExperiment2.py --models "['ModelBsRsdnf']" \
#--kwmodel "{$doeComp,'sizeStream':2000,'pSpike':0.01}"  \
#--nbThread 7  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':[0.0,0.4,0.6,1.0],'nbDistr':[0,3,5]}" \
#--timeEnd 20 --prefix "casas_comp_noise_distr"
#


#python3 runExperiment2.py --models "['ModelBsRsdnf']" \
#--kwmodel "{$casasComp,'sizeStream':[100,500,1000,1500,2000,5000],'pSpike':0.005}"  \
#--nbThread 4  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.4,'nbDistr':3}" \
#--timeEnd 30 --prefix "casas_comp_sizestream_delta05_robust3"

#python3 runExperiment2.py --models "['ModelBsRsdnf']" \
#--kwmodel "{$casasComp}"  \
#--nbThread 7  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.5,'nbDistr':[0,3,5]}" \
#--timeEnd 20 --prefix "casas2_comp_noise5_distr"

#python3 runExperiment2.py --models "['ModelNSpike']" \
#--kwmodel "{$casasComp,'nspike':15}"  \
#--nbThread 7  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.5,'nbDistr':[0,3,5]}" \
#--timeEnd 20 --prefix "nspike2_comp_noise5_distr"

python3 runExperiment2.py --models "['ModelDNF']" \
--kwmodel "{$casasComp}"  \
--nbThread 7  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
--kwscenario "{'noiseI':0.5,'nbDistr':[0,3,5]}" \
--timeEnd 20 --prefix "sdnf2_comp_noise5_distr"






#
#CASAS CNFT
#
#works but very slow
#python3 runExperiment2.py --models "['ModelBsRsdnf']" \ 
#--dt "1e-4" \
#--kwmodel "{$doeCnftComp,'sizeStream':1}"  \
#--nbThread 4  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.4,'nbDistr':3}" \
#--timeEnd 10 --prefix "casasCnft_comp_ss1dt1-4" \


#python3 runExperiment2.py --models "['ModelBsRsdnf']" \
#--dt "[0.1,0.01,0.001]" \
#--kwmodel "{$doeCnftComp,'sizeStream':[1,10,100,1000]}"  \
#--nbThread 4  --scenarios "['ScenarioRobustness']"  --stats "['StatsTracking2']" \
#--kwscenario "{'noiseI':0.4,'nbDistr':3}" \
#--timeEnd 30 --prefix "casasCnft_comp_sizestreamxdt01" \
#

#INFLUENCE de DT sur nbActivation
#python3 runExperiment2.py --models "['ModelDNF']" \
#--dt "[0.1,0.01,0.001]" \
#--kwmodel "{$spikeComp}"  \
#--nbThread 8  --scenarios "['ScenarioRobustness']"  --stats "['StatsNbAct']" \
#--kwscenario "{'noiseI':0.4,'nbDistr':3}" \
#--timeEnd 30 --prefix "spike_dog_dt_act" \

#python3 runExperiment2.py --models "['ModelDNF']" \
#--dt "[0.1,0.01,0.001]"  --size "[35,49,65]" \
#--kwmodel "{$spikeComp,'tau':[0.3,0.6]}"  \
#--nbThread 8  --scenarios "['ScenarioRobustness']"  --stats "['StatsNbAct']" \
#--kwscenario "{'noiseI':0.4,'nbDistr':3}" \
#--timeEnd 30 --prefix "spike_dog_dtxsizextau_act" \

