#include "routerSequence.h"
#include "cellrsdnf.h"
#include <iostream>
#include "param.h"
#include "bitstreamutils.h"

RouterSequence::RouterSequence(int row,int col) : Router(row,col)
{

    this->regs.push_back(Register(false));//RANDOM_OUT

}






void RouterSequence::computeState(){

    int buffer = this->getRegState(BUFFER);
    int nbInput = 0;

    for(unsigned int i = 1 ; i < this->neighbours.size()-1;i++){ //-1 because the last neighbour is one giving the next random bit
        nbInput += this->getNeighbour(i).get()->getRegState(SPIKE_OUT);
    }


    if(buffer > 0 || nbInput > 0 ){

        //std::cout << " test " << std::endl;
        if(this->getRegState(RANDOM_OUT)){
            this->setRegState(SPIKE_OUT,true);

        }else{
            this->setRegState(SPIKE_OUT,false);
        }
        int toAdd = buffer+nbInput-1;
        this->setRegState(BUFFER,toAdd);
    }else{
        this->setRegState(SPIKE_OUT,false);
    }

    //update the random bit from the neighbour
    this->setRegState(RANDOM_OUT,this->getNeighbour(this->neighbours.size()-1).get()->getRegState(RANDOM_OUT));


}
