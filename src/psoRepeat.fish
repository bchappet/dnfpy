#python3 psoRepeat.py PSOClass PSOParamsDict Model Scenario ConstantParamsDict nbEvalMax NbRepeat FileSave

set dir 'expPSO'

set kernel 'DOG'
set scenario 'WorkingMemory'
set repet 50
set name $kernel\_$scenario\_$repet

mkdir $dir/$name
for x in (seq $repet)
        echo $x
        python3 launchPSO.py --scenario $scenario   > $dir/$name/$name\_$x.csv
end

