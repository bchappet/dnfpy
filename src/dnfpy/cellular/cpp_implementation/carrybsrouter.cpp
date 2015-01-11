#include "carrybsrouter.h"
#include "bitstreamutils.h"
CarryBsRouter::CarryBsRouter()
{
    //params
    this->params.push_back(new Param<float>(1.));//PROBA_SYNAPSE
    //registres
    this->regs.push_back(new Register<bool>(0));//BS_OUT
    this->regs.push_back(new Register<bool>(0));//CARRY
}

void CarryBsRouter::computeState(){
    bool res = false;
    bool carry = this->getRegState<bool>(CarryBSRouter_Registers::CARRY);
    bool nextCarry = carry;
    //multiplication per synaptic weight
    bool synaptiWeightBS = generateStochasticBit(this->getParam<float>(CarryBSRouter_Parameters::PROBA_SYNAPSE));
    if(synaptiWeightBS){
        bool neigh = false;

        int sumNeigh = 0;
        for(Module* mod:this->neighbours){
            bool neighState = mod->getRegState<bool>(0);
            neigh |= neighState;//rough addition of inputs
            sumNeigh += neighState;
        }
        res = carry | neigh;
        sumNeigh += carry;
        nextCarry =sumNeigh > 1;
    }
    this->setRegState<bool>(CarryBSRouter_Registers::BS_OUT,res);
    this->setRegState<bool>(CarryBSRouter_Registers::CARRY,nextCarry);
}

