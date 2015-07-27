#include "cellgof.h"
#define STATE 0
#include <iostream>

CellGof::CellGof(bool state): Module()
{
    this->regs.push_back(Register(state));//STATE
}

void CellGof::computeState(){
    bool alive = this->getRegState(STATE);
    int nbNeighAlive = 0;

    for(unsigned int i = 0 ; i < this->neighbours.size() ; i++){
        nbNeighAlive += this->neighbours[i].get()->getRegState(STATE);
    }
    //std::cout << "nbInput : " << this->inputs.size() << std::endl;
    //std::cout << "nbNeighAlive : " << nbNeighAlive << std::endl;

    if(alive){
        if(nbNeighAlive < 2 || nbNeighAlive > 3){
            this->setRegState(STATE,false);
        }else{
            //stay alive
        }
    }else{
        if(nbNeighAlive == 3){
            this->setRegState(STATE,true);
        }
    }
}
