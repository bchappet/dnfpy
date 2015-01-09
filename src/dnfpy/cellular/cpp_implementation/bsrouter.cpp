#include "bsrouter.h"
#include "bitstreamutils.h"
#include <iostream>
BSRouter::BSRouter()
{
    //params
    this->params.push_back(new Param<float>(1.));//PROBA_SYNAPSE
    //registres
    this->regs.push_back(new Register<bool>(0));//BS_OUT
}

void BSRouter::computeState(){
    bool res = false;
    //multiplication per synaptic weight
    bool synaptiWeightBS = generateStochasticBit(this->getParam<float>(BSRouter_Parameters::PROBA_SYNAPSE));
    if(synaptiWeightBS){
        int i = 0;
        for(Module* mod:this->neighbours){
            res |= mod->getRegState<bool>(0);//rough addition of inputs
           // std::cout << "i: " << i << " res : " << res << std::endl;
            i++;

        }
    }
    this->setRegState<bool>(BSRouter_Registers::BS_OUT,res);
}


