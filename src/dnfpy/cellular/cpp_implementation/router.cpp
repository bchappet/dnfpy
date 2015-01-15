#include "router.h"
#include "cellrsdnf.h"
#include <iostream>
#include "param.h"
#include "bitstreamutils.h"

Router::Router()
{
    //params:
    this->params.push_back(new Param<int>(20));//NB_SPIKE
    this->params.push_back(new Param<float>(1.0));//PROBA
    //registres
    this->regs.push_back(new Register<int>(0));//BUFFER
    this->regs.push_back(new Register<bool>(false));//SPIKE_OUT

}



void Router::setActivated(bool isActivated){
    this->activated = isActivated;
}

void Router::computeState(){

    int buffer = this->getRegState<int>(BUFFER);
    int nbInput = 0;
    for(unsigned int i = 1 ; i < this->neighbours.size();i++){
        Module* mod = this->getNeighbour(i);
        nbInput += mod->getRegState<bool>(SPIKE_OUT);
    }

    bool activated = this->activated;

//    if(nbInput > 0){
//        std::cout << "nbInput : " << nbInput << std::endl;
//    }

    if(buffer > 0 || nbInput > 0 || activated){
        if(generateStochasticBit(this->getParam<float>(PROBA))){
            this->setRegState<bool>(SPIKE_OUT,true);
        }else{
            this->setRegState<bool>(SPIKE_OUT,false);
        }
        int toAdd = buffer+nbInput-1;
        if(activated){
            toAdd += this->getParam<int>(NB_SPIKE);

            //std::cout << "Activated to add : " << toAdd <<  std::endl;
        }
        this->setRegState<int>(BUFFER,toAdd);
    }else{
        this->setRegState<bool>(SPIKE_OUT,false); 
    }


}