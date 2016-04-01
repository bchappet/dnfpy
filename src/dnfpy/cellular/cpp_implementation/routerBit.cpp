#include "routerBit.h"
#include "cellrsdnf.h"
#include <iostream>
#include "param.h"
#include "bitstreamutils.h"

RouterBit::RouterBit(int row,int col) : Router(row,col)
{
    this->randomBit = true;
}



void RouterBit::computeState(){

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

        if(this->randomBit){
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


void RouterBit::setAttribute(int index,void* value){
    if(index == RANDOM_BIT)
        this->randomBit = *((bool*)value);
    else{
        std::cout << " error " << index << "not good " << std::endl;
        exit(-1);
    }

}

void RouterBit::getAttribute(int index,void* value){
    if(index == RANDOM_BIT)
        *((bool*)value) = this->randomBit;
    else{
        std::cout << " error " << index << "not good " << std::endl;
        exit(-1);
    }
}

