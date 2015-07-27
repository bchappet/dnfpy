#include "carrybsrouter.h"
#include "bitstreamutils.h"
#include <iostream>
#include "cellbsrsdnf.h"
CarryBsRouter::CarryBsRouter()
{



    //registres
    this->regs.push_back(Register(0));//BS_OUT
    this->regs.push_back(Register(0));//CARRY
}

void CarryBsRouter::computeState(){
    bool res = false;
    bool carry = this->getRegState(CarryBSRouter_Registers::CARRY);
    bool nextCarry = carry;
    //multiplication per synaptic weight
    bool synaptiWeightBS = generateStochasticBit(this->getParam<float>(CellBsRsdnf::PROBA_SYNAPSE),
                                                this->getParam<int>(CellBsRsdnf::PRECISION_PROBA));

    if(synaptiWeightBS){
        bool neigh = false;

        int sumNeigh = 0;
        for(ModulePtr mod:this->neighbours){
            bool neighState = mod.get()->getRegState(0);
            neigh |= neighState;//rough addition of inputs
            sumNeigh += neighState;
        }
        res = carry | neigh;
        sumNeigh += carry;
        nextCarry =sumNeigh > 1;

    }
    this->setRegState(CarryBSRouter_Registers::BS_OUT,res);
    this->setRegState(CarryBSRouter_Registers::CARRY,nextCarry);
}

void CarryBsRouter::setLastRandomNumber(int* intp){
    this->lastRandomNumber = intp;
}
