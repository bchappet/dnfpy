#include "cellgof.h"
#define STATE 0
#include <iostream>

CellGof::CellGof(bool state): Module()
{
    this->regs.push_back(new Register<bool>(state));//STATE
}

void CellGof::computeState(){
    bool alive = this->getRegState<bool>(STATE);
    int nbNeighAlive = 0;
    for(Module* in:this->inputs){
        nbNeighAlive += in->getRegState<bool>(STATE);
    }
    //std::cout << "nbInput : " << this->inputs.size() << std::endl;
    //std::cout << "nbNeighAlive : " << nbNeighAlive << std::endl;

    if(alive){
        if(nbNeighAlive < 2 || nbNeighAlive > 3){
            this->setRegState<bool>(STATE,false);
        }else{
            //stay alive
        }
    }else{
        if(nbNeighAlive == 3){
            this->setRegState<bool>(STATE,true);
        }
    }
}
