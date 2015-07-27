#include "bsrouter.h"
#include "bitstreamutils.h"
#include <iostream>
#include "cellbsrsdnf.h"
BSRouter::BSRouter()
{

    //registres
    this->regs.push_back(Register(0));//BS_OUT

}



void BSRouter::computeState(){
    bool res = false;
    //multiplication per synaptic weight

    bool synaptiWeightBS = generateStochasticBit(this->getParam<float>(CellBsRsdnf::PROBA_SYNAPSE),
                                                this->getParam<int>(CellBsRsdnf::PRECISION_PROBA));

    if(synaptiWeightBS){
        //int i = 0;
        for(ModulePtr mod:this->neighbours){
            res |= mod.get()->getRegState(0);//rough addition of inputs
           // std::cout << "i: " << i << " res : " << res << std::endl;
           // i++;

        }
    }
    this->setRegState(BSRouter_Registers::BS_OUT,res);
}

void BSRouter::setLastRandomNumber(int* intp){
    this->lastRandomNumber = intp;
}
