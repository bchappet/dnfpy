# Bugs 

10/03/16
. NSpike behaves differently from rsdnf in a static scenario. 

The condition for equality of behaviour is to respect the worst case scenario of transmission time
$dt = \pi N + 2*res$ and $\pi = 0.01 res^2 + 1.95$


Experiment:
python3 main.py --model ModelNSpike --scenario ScenarioStatic --params "{'nspike':20,'pExc':0.11,'iExc':1.19,'iInh':0.8}" --stats StatsTracking --size 49
max act was 74 clkRatio = 116*20 + 2*49 = 
python3 main.py --model ModelNSpike --scenario ScenarioStatic --params "{'nspike':20,'pExc':0.11,'iExc':1.19,'iInh':0.8,'cell':'Rsdnf','clkRatio':2418}" --size 49 --stats StatsTracking
python3 main.py --model ModelNSpike --scenario ScenarioStatic --params "{'nspike':20,'pExc':0.11,'iExc':1.19,'iInh':0.8,'cell':'Rsdnf','clkRatio':2418,'routerType':'prng'}" --size 49 --stats StatsTracking


Bug resolved. The amount of spikes was underestimated


