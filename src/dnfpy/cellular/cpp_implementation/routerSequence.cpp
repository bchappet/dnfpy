#include "routerSequence.h"
#include "cellrsdnf.h"
#include <iostream>
#include "param.h"
#include "bitstreamutils.h"

RouterSequence::RouterSequence() : Router()
{

    this->regs.push_back(Register(false));//RANDOM_OUT

}






void RouterSequence::computeState(){

    int buffer = this->getRegState(BUFFER);
    int nbInput = 0;

    for(unsigned int i = 1 ; i < this->neighbours.size()-1;i++){
        nbInput += this->getNeighbour(i).get()->getRegState(SPIKE_OUT);
    }

    bool activated = this->activated;

//    if(nbInput > 0){
//        std::cout << "nbInput : " << nbInput << std::endl;
//    }

    if(buffer > 0 || nbInput > 0 || activated){

        //std::cout << " test " << std::endl;
        if(this->getRegState(RANDOM_OUT)){
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

    //update the random bit from the neighbour
    this->setRegState(RANDOM_OUT,this->getNeighbour(this->neighbours.size()-1).get()->getRegState(RANDOM_OUT));


}
