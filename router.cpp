#include "router.h"
#include "cellrsdnf.h"
#include <iostream>
//registers


Router::Router()
{
    this->regs.push_back(new Register<int>(0));//BUFFER
    this->regs.push_back(new Register<bool>(false));//SPIKE_OUT

}

void Router::computeState(){

    int buffer = this->getRegState<int>(BUFFER);

    int nbInput = 0;

    for(unsigned int i = 1 ; i < this->inputs.size();i++){
        Module* mod = this->getInput(i);
        nbInput += mod->getRegState<bool>(SPIKE_OUT);
    }

    bool activated = this->getInput(0)->getRegState<bool>(CellRsdnf::ACTIVATED_OUT);

//    if(nbInput > 0){
//        std::cout << "nbInput : " << nbInput << std::endl;
//    }

    if(buffer > 0 || nbInput > 0 || activated){
        this->setRegState<bool>(SPIKE_OUT,true);
        int toAdd = buffer+nbInput-1;
        if(activated){

            toAdd += Router::NB_SPIKE;
            //std::cout << "Activated to add : " << toAdd <<  std::endl;
        }
        this->setRegState<int>(BUFFER,toAdd);
    }else{
        this->setRegState<bool>(SPIKE_OUT,false);
        this->setRegState<int>(BUFFER,0);
    }


}
