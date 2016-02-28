#Precision proba = 8
!python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 10 10 BsRSDNF_precision_50 log7 4
python extractMeanStd.py BsRSDNF_precision_50.csv BsRSDNF_precision_10 10

#precisionProba 30
!python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioDistracters']" 10 10 BsRSDNF_precision_10 log8 8

#routerType=uniformCell, sizeStream = 100,200 pSpike=0.1, 
#self,size,dt=0.1,sizeStream=100,pSpike=0.1,routerType="uniformCell",
#             precisionProba=30,reproductible=False,iInh=0.9,iExc=1.5):
!python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRSDNFUniform_sizeStream_50 log9 8
#great success!
python extractMeanStd.py BsRSDNFUniform_sizeStream_50.csv BsRSDNFUniform_sizeStream_50 50
#great success!
python plotMeanStd.py  BsRSDNFUniform_sizeStream_50_std.csv  BsRSDNFUniform_sizeStream_50 ErrorDist scenario sizeStream
#great success!


#Precision with size stream 100
!python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRSDNFUniform_sizeStream10_precision8_50 log10 8

#Agregation NSpike+BsRsdnfUniform bar width = 0.4
python plotMeanStd.py NSpike_BsRsdnfUniform_std.csv NSpike_BsRsdnfUniform ErrorDist sizeStream model



!python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRSDNFitted_sizeStream100_scenario_50 log12 8
python extractMeanStd.py  BsRSDNFitted_sizeStream100_scenario_50.csv BsRSDNFitted_sizeStream100_scenario_50 50
python plotMeanStd.py BsRSDNFitted_sizeStream100_scenario_50_std.csv BsRSDNFitted_sizeStream100_scenario_50 ErrorDist  scenario model

#after optimization algo gen, scenario Robustness ate switching error and well clusterized sp=0.1
#[1.96, 0.93, 4.826123183649009e-05, 3.712402448960776]
!python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRSDN_GA_sizeStream100_scenario_50 log12 8
python extractMeanStd.py  BsRSDN_GA_sizeStream100_scenario_50.csv  BsRSDN_GA_sizeStream100_scenario_50  50
python plotMeanStd.py BsRSDN_GA_sizeStream100_scenario_50_std.csv BsRSDN_GA_sizeStream100_scenario_50 ErrorDist  scenario model


#after optimization algo gen, scenario Robustness ate switching error and well clusterized sp=0.05 sizeStream 500
#[1.5735619684700972,0.7466390972842809,1.3e-05,1.0]
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRSDN_GA_sizeStream500_scenario_50 log13 8
python extractMeanStd.py  BsRSDN_GA_sizeStream500_scenario_50.csv  BsRSDN_GA_sizeStream500_scenario_50  50
python plotMeanStd.py BsRSDN_GA_sizeStream500_scenario_50_std.csv BsRSDN_GA_sizeStream500_scenario_50 ErrorDist  scenario model

#Try best ind algo gen fast p=0.1
#[4.029, 3.861, 0.242, 1.065]
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 30 10 SBSFast_GA_sizeStream100_scenario_30 log14 8 "{'size':49,'pSpike':0.1,'sizeStream':100,'iExc':4.029,'iInh':3.861,'pExc':0.242,'pInh':1.065,'mapType':'fast'}"
python extractMeanStd.py  SBSFast_GA_sizeStream100_scenario_30.csv   SBSFast_GA_sizeStream100_scenario_30  30
python plotMeanStd.py SBSFast_GA_sizeStream100_scenario_30_std.csv  SBSFast_GA_sizeStream100_scenario_30 ErrorDist  scenario model

#The same with 100 iterations fast
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 100 10 SBSDoubleFast_GA_sizeStream100_scenario_100 log14 8 "{'size':49,'pSpike':0.1,'sizeStream':100,'iExc':4.029,'iInh':3.861,'pExc':0.242,'pInh':1.065,'mapType':'fast'}"
python extractMeanStd.py  SBSDoubleFast_GA_sizeStream100_scenario_100.csv   SBSFast_GA_sizeStream100_scenario_100  100
python plotMeanStd.py SBSFast_GA_sizeStream100_scenario_100_std.csv  SBSFast_GA_sizeStream100_scenario_100 ErrorDist  scenario model


#[1.763, 1.689, 0.223, 0.983]
#try another ind of same opt
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 100 10 SBSFast_GA2_sizeStream100_scenario_100 log15 8 "{'size':49,'pSpike':0.1,'sizeStream':100,'iExc':1.763,'iInh':1.689,'pExc':0.223,'pInh':0.983,'mapType':'fast'}"
python extractMeanStd.py SBSFast_GA2_sizeStream100_scenario_100.csv SBSFast_GA2_sizeStream100_scenario_100 100
python plotMeanStd.py SBSFast_GA2_sizeStream100_scenario_100_std.csv SBSFast_GA2_sizeStream100_scenario_100 ErrorDist scenario model
#Not as good as the other one

#The same with different precision
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 SBSFast_GA_sizeStream100_precision2_50 log14 8 "{'precisionProba':[1,2,3,4,5,6,7,8,9,10,20,31],'size':49,'pSpike':0.1,'sizeStream':100,'iExc':4.029,'iInh':3.861,'pExc':0.242,'pInh':1.065,'mapType':'fast'}"
python extractMeanStd.py SBSFast_GA_sizeStream100_precision2_50.csv SBSFast_GA_sizeStream100_precision2_50 50
python plotMeanStd.py SBSFast_GA_sizeStream100_precision2_50_std.csv SBSFast_GA_sizeStream100_precision2_50 ErrorDist scenario precisionProba

#
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 SBSFast_GA2_sizeStream100_correlated_50 log14 4 "{'precisionProba':8,'size':49,'pSpike':0.1,'sizeStream':100,'iExc':4.029,'iInh':3.861,'pExc':0.242,'pInh':1.065,'mapType':'doublefast','shift':[0,1,3,5,10,20]}"
python extractMeanStd.py  SBSFast_GA2_sizeStream100_correlated_50.csv  SBSFast_GA2_sizeStream100_correlated_50 50
python plotMeanStd.py  SBSFast_GA2_sizeStream100_correlated_50_std.csv  SBSFast_GA2_sizeStream100_correlated_50 ErrorDist scenario shift





################################################Changed scenario with normalization ############################################################
#compare best CNFT vs best Spike
python runExperiment.py "['ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 CNFTvsSDNF1_scenario_50 log15 4 "{'model':'cnft','size':49}"
python runExperiment.py  "['ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 CNFTvsSDNF2_scenario_50 log15 4 "{'model':'spike','size':49}"
cat CNFTvsSDNF1_scenario_50.csv >> CNFTvsSDNF_scenario_50.csv
cat CNFTvsSDNF2_scenario_50.csv >> CNFTvsSDNF_scenario_50.csv
python extractMeanStd.py CNFTvsSDNF_scenario_50.csv CNFTvsSDNF_scenario_50


python runExperiment.py "['ModelDNF']" "[]"  "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 SDNDF_step_50 log15 8 "{'model':'spike','size':49,'nbStep':[1,2,3,4,5,6,10,20,0]}"

python runExperiment.py "['ModelDNF']" "[]"  "['ScenarioTracking','ScenarioRobustness','ScenarioSwitch']" 50 10 SDNDFswitch_step_50 log16 8 "{'iExc': 0.75251497895837283, 'wInh': 0.80920671377141562, 'iInh': 0.38538068898980515, 'model': 'spike', 'size': 49, 'wExc': 0.10285131451500595,'nbStep':[1,2,3,4,5,6,10,20,0]}"


################################22/04/2015 paper 5 CASAS-DNF final version  ###################################################################
#The optimization tools being ready, we optimized RSDNF and deduced parameters of CASAS with curve fitting:
#NSpike PSO
python runExperiment.py "['ModelNSpike']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 NSpike_PSO_scenario_50 log1 8 "{'iExc': 1.483, 'pExc': 0.015, 'pInh': 0.561, 'iInh': 0.967, 'size': 49}"
#CASAS fitting: {'iExc': 2.378133244010106, 'wInh': 1.575986981897518, 'iInh': 1.443869210918792, 'wExc': 0.00011225251356013395}
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRsdnf_fit1_scenario_50 log1 8 "{'iExc': 2.3781, 'pInh': 1.57599, 'iInh': 1.443869, 'pExc': 0.00011225,'mapType':'fast','sizeStream':100,'size':49,'pSpike':0.1}"
#CASAS PSO
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRsdnf_PSO_scenario_50 log1 8 "{'iExc': 1.4733, 'pExc': 0.0135, 'pInh': 0.9763, 'iInh': 1.1228, 'mapType': 'fast', 'size': 49,'sizeStream':100,'pSpike':0.1}"

#merge everything
touch compareFitPso.csv
cat NSpike_PSO_scenario_50.csv >> compareFitPso.csv 
cat BsRsdnf_fit1_scenario_50.csv >> compareFitPso.csv 
cat BsRsdnf_PSO_scenario_50.csv >> compareFitPso.csv 
#edit a bit
#a bit of edditing
python extractMeanStd.py compareFitPso.csv compareFitPso 50
python plotMeanStd.py compareFitPso_std.csv compareFitPso  ErrorDist scenario model
eog compareFitPso.png
#intersesting, it is bad for noise but not for sistracters

####################################23/04/2015######################
#TRY again adding noise iscenario to PSO
#CASAS {'iExc': 2.1172900564613077, 'pExc': 0.061770729098476002, 'pInh': 0.46681555470642633, 'iInh': 1.8631989487485867, 'mapType': 'fast', 'sizeStream': 100, 'size': 49}
#NSpike {'iExc': 1.7621191360285322, 'pExc': 0.038709422720724092, 'pInh': 0.71825131515352136, 'iInh': 1.30363349837411, 'size': 49}

python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRsdnf_PSO2_scenario_50 log1 8 "{'iExc': 2.1173, 'pExc': 0.0618, 'pInh': 0.4668, 'iInh': 1.8632, 'mapType': 'fast', 'size': 49,'sizeStream':100,'pSpike':0.1}"
python runExperiment.py "['ModelNSpike']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 NSpike_PSO2_scenario_50 log1 8 "{'iExc': 1.7621, 'pExc': 0.0397, 'pInh': 0.7183, 'iInh': 1.3036, 'size': 49}"
touch pso2_scenario.csv
cat BsRsdnf_PSO2_scenario_50.csv >> pso2_scenario.csv
cat NSpike_PSO2_scenario_50.csv >> pso2_scenario.csv

python extractMeanStd.py pso2_scenario.csv pso2_scenario 50 
python plotMeanStd.py pso2_scenario_std.csv pso2_scenario ErrorDist scenario model


#Au final on prend param par default pour NSpike et PSO1 pour CAsas
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRsdnf_PSO_scenario_50_2 log1 8 "{'iExc': 1.4733, 'pExc': 0.0135, 'pInh': 0.9763, 'iInh': 1.1228, 'mapType': 'fast', 'size': 49,'sizeStream':100,'pSpike':0.1}"
#iExc=1.25,iInh=0.7,pExc=0.0043,pInh=0.9
python runExperiment.py "['ModelNSpike']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 100 10 NSpike_default_scenario_100 log1 8 "{'iExc': 1.25, 'pExc': 0.0043, 'pInh': 0.9, 'iInh': 0.7, 'size': 49}"

#Noise resistant
#{'iExc': 1.1557043521797394, 'pExc': 0.035189624636426727, 'pInh': 0.99737931137438129, 'iInh': 0.86936211343564351, 'mapType': 'fast', 'sizeStream': 100, 'size': 49}
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRsdnf_PSONoise_scenario_50 log1 8 "{'iExc': 1.1557, 'pExc': 0.0352, 'pInh': 0.9974, 'iInh': 0.8694, 'mapType': 'fast', 'size': 49,'sizeStream':100,'pSpike':0.1}"

touch fig8_final_50.csv
cat BsRsdnf_PSONoise_scenario_50.csv >> fig8_final_50.csv
cat NSpike_default_scenario_50.csv >> fig8_final_50.csv
python extractMeanStd.py fig8_final_50.csv fig8_final_50 50
python plotMeanStd.py fig8_final_50_std.csv fig8_final_50 ErrorDist scenario model
eog fig8_final_50.png ##################GOOD


###########################################################
python runExperiment.py "['ModelNSpike']" "[]" "['ScenarioDistracters']" 50 10 NSpike_default_size_50 log2 8 "{'iExc': 1.25, 'pExc': 0.0043, 'pInh': 0.9, 'iInh': 0.7, 'size': 49,'nspike':[1,3,5,10,20]}"
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioDistracters']" 50 10 BsRsdnf_PSONoise_size_50 log2 8 "{'iExc': 1.1557, 'pExc': 0.0352, 'pInh': 0.9974, 'iInh': 0.8694, 'mapType': 'fast', 'size': 49,'pSpike':0.1,'sizeStream':[10,30,50,100,200]}"
touch fig8_size_50.csv
cat BsRsdnf_PSONoise_size_50.csv >> fig8_size_50.csv
cat NSpike_default_size_50.csv >> fig8_size_50.csv
python extractMeanStd.py fig8_size_50.csv fig8_size_50 50
python plotMeanStd.py fig8_size_50_std.csv fig8_size_50   ErrorDist sizeStream model
#


cp fig8_final_50.eps ~/Dropbox/THESE/Redaction/article5_CASAS_DNF/fig/fig8Scenario.eps
cp fig8_size_50.eps ~/Dropbox/THESE/Redaction/article5_CASAS_DNF/fig/fig8Size.eps


touch fig8_final.csv
cat BsRsdnf_PSO_scenario_100.csv >> fig8_final.csv
cat NSpike_default_scenario_100.csv >> fig8_final.csv
python extractMeanStd.py fig8_final.csv fig8_final 100
python plotMeanStd.py fig8_final_std.csv fig8_final ErrorDist scenario model
eog fig8_final.png
evince fig8_final.eps



################Conclusion : on utilise pso!!##########################"
#Fig 8 (b)
#TODO plot casas vs dnf
cp compareFitPso_std.csv fig8Scenario_std.csv
python plotMeanStd.py fig8Scenario_std.csv compareFitPso  ErrorDist scenario model
#It appear that the model NSpike is less performent than the previous parameters. Maybe we shoukld optimize with the three scenario


#Fig. 8 (a): different size stream
python runExperiment.py "['ModelNSpike']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 NSpike_PSO_scenarioxSize_50 log2 8 "{'iExc': 1.483, 'pExc': 0.015, 'pInh': 0.561, 'iInh': 0.967, 'size': 49,'nspike':[1,3,5,10,20]}"
python runExperiment.py "['ModelBsRsdnf']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 BsRsdnf_PSO_scenarioxSize_50 log2 8 "{'iExc': 1.4733, 'pExc': 0.0135, 'pInh': 0.9763, 'iInh': 1.1228, 'mapType': 'fast', 'size': 49,'pSpike':0.1,'sizeStream':[10,30,50,100,200]}"
touch fig8ScenarioxSize.csv
cat NSpike_PSO_scenarioxSize_50.csv >> fig8ScenarioxSize.csv
cat BsRsdnf_PSO_scenarioxSize_50.csv >> fig8ScenarioxSize.csv
python extractMeanStd.py fig8ScenarioxSize_Tracking.csv fig8ScenarioxSize_Tracking 50
python extractMeanStd.py fig8ScenarioxSize_Noise.csv fig8ScenarioxSize_Noise 50
python extractMeanStd.py fig8ScenarioxSize_Distracters.csv fig8ScenarioxSize_Distracters 50

python plotMeanStd.py fig8ScenarioxSize_Tracking_std.csv fig8ScenarioxSize_Tracking   ErrorDist sizeStream model
python plotMeanStd.py fig8ScenarioxSize_Noise_std.csv fig8ScenarioxSize_Noise   ErrorDist sizeStream model
python plotMeanStd.py fig8ScenarioxSize_Distracters_std.csv fig8ScenarioxSize_Distracters   ErrorDist sizeStream model
###BsRsdnf not very resistant to noise with  when sizeStream = 50




#10/04/2015
#######Spike frequency adaptation for distracter robust tracking####
python runExperiment.py "['ModelSFA','ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 SFA1_scenario_50 log1 4 "{'model':'cnft','size':49}"
python extractMeanStd.py  SFA1_scenario_50.csv SFA1_scenario_50 50
python plotMeanStd.py SFA1_scenario_50_std.csv SFA1_scenario_50  ErrorDist model scenario 

#SFA for obstacles################################
python runExperiment.py "['ModelSFA',]" "[]" "['ScenarioTracking','ScenarioDistracters']" 50 22 SFA_obstacles_50 log2 8 "{'model':'spike','size':49,'obsSize':[0,0.1,0.2,0.3,0.4,0.5]}"
python extractMeanStd.py SFA_obstacles_50.csv SFA_obstacles_50 50
python plotMeanStd.py  SFA_obstacles_50_std.csv  SFA_obstacles_50 ErrorDist scenario obsSize


#26/08/2015 Manuscrit

##DNF DOL
python experiments/runExperiment.py "['ModelDNFLin','ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 Lin_scenario_50 log1 6 "{'model':'spike','size':49}"
python experiments/extractMeanStd.py  Lin_scenario_50.csv Lin_scenario_50 50
python experiments/plotMeanStd.py Lin_scenario_50_std.csv Lin_scenario_50  ErrorDist scenario model

##DNF DOE
#indiv: {'iExc': 4.52, 'iInh': 3.96, 'pExc': 0.13, 'pInh': 0.45}
python runExperiment.py "['ModelDNFExp','ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 Exp_scenario_50 log1 6 "{'model':'spike','size':49}"
python extractMeanStd.py  Exp_scenario_50.csv Exp_scenario_50 50
python plotMeanStd.py Exp_scenario_50_std.csv Exp_scenario_50  ErrorDist scenario model
cp Exp_scenario_50.png ~/manu/fig/

##DNF NSpike
python runExperiment.py "['ModelNSpike']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 NSpike_nspike_scenario_50 log1 4 "{'size':49,'iExc': 4.52, 'iInh': 3.96, 'pExc': 0.13, 'pInh': 0.45,'nspike':[1,2,3,5,7,10,15,20,30]}"
python extractMeanStd.py  NSpike_nspike_scenario_50.csv NSpike_nspike_scenario_50 50
python plotMeanStd.py NSpike_nspike_scenario_50_std.csv NSpike_nspike_scenario_50  ErrorDist  nspike scenario
cp NSpike_nspike_scenario_50.png ~/manu/fig/


########Petit intermède pour tester la PSO (voir optimisation.tex) ####
repet=50

####The control is DNF  {'iExc' : 1.25,'iInh' : 0.7,'wExc' : 0.1,'wInh': 0.9}
name=control_SDNF_50
python runExperiment.py "['ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" $repet 10 $name log1 6 "{'iExc' : 1.25,'iInh' : 0.7,'wExc' : 0.1,'wInh': 0.9,'size':49,'model':'spike','activation':'step'}"
python extractMeanStd.py  ${name}.csv $name $repet
python plotMeanStd.py "'${name}_std.csv'" $name  ErrorDist scenario model

#test multidata plot
python plotMeanStd.py "['${name}_std.csv','${name}_std.csv']" $name  ErrorDist scenario model "[{},{'ModelDNF':'ModelDNF2'}]"



name=psoBestDOG_scenario
python runExperiment.py "['ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" $repet 10 $name log1 6 "{'iExc': 0.6882535042131549, 'wInh': 0.98481994656567062, 'iInh': 0.36901503942662878, 'activation': 'step', 'size': 49, 'model': 'spike', 'wExc': 0.12621525686191745}"
python extractMeanStd.py  ${name}.csv $name $repet
python plotMeanStd.py "['${name}_std.csv','control_SDNF_50_std.csv']" $name  ErrorDist scenario model "[{},{'ModelDNF':'Control'}]"
cp ${name}.png ~/manu/organisation/fig/



name=psoRobustnessBestDOG_scenario
python runExperiment.py "['ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" $repet 10 $name log1 6 "{'iExc': 1.4333616829100384, 'wInh': 0.40258922624680027, 'iInh': 1.2137286676873005, 'activation': 'step', 'size': 49, 'model': 'spike', 'wExc': 0.23497103229353747}"
python extractMeanStd.py  ${name}.csv $name $repet
python plotMeanStd.py "['${name}_std.csv','psoBestDOG_scenario_std.csv','control_SDNF_50_std.csv']" $name  ErrorDist scenario model "[{'ModelDNF':'PSONoise'},{'ModelDNF':'PSORobustness'},{'ModelDNF':'Control'}]"
cp ${name}.png ~/manu/organisation/fig/



name=pso2ScenarioBestDOG_scenario
python runExperiment.py "['ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" $repet 10 $name log1 6 "{'iExc': 0.53321517218276715, 'wInh': 0.97571839835193952, 'iInh': 0.19702998086884074, 'activation': 'step', 'size': 49, 'model': 'spike', 'wExc': 0.096521191373136625}"
python extractMeanStd.py  ${name}.csv $name $repet
python plotMeanStd.py "['${name}_std.csv','psoRobustnessBestDOG_scenario_std.csv','psoBestDOG_scenario_std.csv','control_SDNF_50_std.csv']" $name  ErrorDist scenario model "[{'ModelDNF':'Model3Scenario'},{'ModelDNF':'PSONoise'},{'ModelDNF':'PSORobustness'},{'ModelDNF':'Control'}]"
cp ${name}.png ~/manu/organisation/fig/


#####################################################Papier ECANN#################################
repet=50
name=DNF_scenario_dx_50
python extractMeanStd2.py DNF_scenario_dx_50.csv DNF_scenario_dx_50 50
python plotMeanStd.py "['DNF_scenario_dx_50_std.csv']" DNF_scenario_dx_50 ErrorDist scenario size


#####################################################Papier ESANN#########################################
python3 runExperiment.py "['ModelNSpike']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 50 10 NSpike_model_scenario_50  log 6 "{}"
