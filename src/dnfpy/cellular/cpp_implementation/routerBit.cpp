#include "routerBit.h"
#include "cellrsdnf.h"
#include <iostream>
#include "param.h"
#include "bitstreamutils.h"

RouterBit::RouterBit(int row,int col) : Router(row,col)
{
    //no registre nor param
    this->randomBit = true;

}

void RouterBit::setRandomBit(bool bit){
    this->randomBit = bit;
}




void RouterBit::setDefaultParams(Module::ParamsPtr params){
    //there are no params in this rrouter

}

void RouterBit::computeState(){

    int buffer = this->getRegState(BUFFER);
    int nbInput = 0;

    for(unsigned int i = 1 ; i < this->neighbours.size();i++){
        nbInput += this->getNeighbour(i).get()->getRegState(SPIKE_OUT);
    }


//    if(nbInput > 0){
//        std::cout << "nbInput : " << nbInput << std::endl;
//    }

    if(buffer > 0 || nbInput > 0 ){

        if(this->randomBit){
            this->setRegState(SPIKE_OUT,true);

        }else{
            this->setRegState(SPIKE_OUT,false);
        }
        int toAdd = buffer+nbInput-1;
        this->setRegState(BUFFER,toAdd);
    }else{
        this->setRegState(SPIKE_OUT,false);
    }


}
