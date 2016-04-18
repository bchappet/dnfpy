#include "bsrouter.h"
#include "bitstreamutils.h"
#include <iostream>
#include "cellbsrsdnf.h"
BSRouter::BSRouter()
{

    //registres
    this->regs.push_back(Register(0,1));//BS_OUT

}


void BSRouter::setDefaultParams(Module::ParamsPtr params){
    params->push_back(new float(1.0));//PROBA_SYNAPSE
    params->push_back(new long int(PRECISION_MAX));//PRECISION_PROBA
}


void BSRouter::computeState(){
    bool res = false;
    //multiplication per synaptic weight

    bool synaptiWeightBS = generateStochasticBit(this->getParam<float>(BSRouter::PROBA_SYNAPSE),
                                                this->getParam<int>(BSRouter::PRECISION_PROBA));

    if(synaptiWeightBS){
        //int i = 0;
        for(ModulePtr mod:this->neighbours){
            res |= mod.get()->getRegState(0);//TODO massive gotcha THE BS_OUT registre has to be the first one!
           // std::cout << "i: " << i << " res : " << res << std::endl;
           // i++;

        }
    }
    this->setRegState(BSRouter_Registers::BS_OUT,res);
}

void BSRouter::setLastRandomNumber(int* intp){
    this->lastRandomNumber = intp;
}
