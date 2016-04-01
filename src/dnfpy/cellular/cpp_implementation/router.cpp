#include "router.h"
#include "cellrsdnf.h"
#include <iostream>
#include "param.h"
#include "bitstreamutils.h"

Router::Router(int row,int col) : Module(row,col)
{

    //attribute
    this->activated = false;

    //registres
    this->regs.push_back(Register(0));//BUFFER
    this->regs.push_back(Register(false));//SPIKE_OUT

}





void Router::setActivated(bool isActivated){
    this->activated = isActivated;
}

void Router::computeState(){

    int buffer = this->getRegState(BUFFER);
    int nbInput = 0;

    for(unsigned int i = 1 ; i < this->neighbours.size();i++){
        nbInput += this->getNeighbour(i).get()->getRegState(SPIKE_OUT);
    }

    bool activated = this->activated;

//    if(nbInput > 0){
//        std::cout << "nbInput : " << nbInput << std::endl;
//    }

    if(buffer > 0 || nbInput > 0 || activated){

        if(generateStochasticBit(this->getParam<float>(CellRsdnf::PROBA),this->getParam<int>(CellRsdnf::PRECISION_PROBA))){
            this->setRegState(SPIKE_OUT,true);

        }else{
            this->setRegState(SPIKE_OUT,false);
        }
        int toAdd = buffer+nbInput-1;
        if(activated){
            toAdd += this->getParam<int>(CellRsdnf::NB_SPIKE);

            //std::cout << "Activated to add : " << toAdd <<  std::endl;
        }
        this->setRegState(BUFFER,toAdd);
    }else{
        this->setRegState(SPIKE_OUT,false);
    }


}
