#include "routerSequenceMixte.h"
#include "cellrsdnf.h"
#include <iostream>
#include "param.h"
#include "bitstreamutils.h"
#include "neumannconnecter.h"

RouterSequenceMixte::RouterSequenceMixte(int row,int col) : RouterSequence(row,col){


}

void  RouterSequenceMixte::computeState(){

    int buffer = this->getRegState(BUFFER);
    int nbInput = 0;

    for(unsigned int i = 1 ; i < this->neighbours.size()-1;i++){ //-1 because the last neighbour is one giving the next random bit
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

    //update the random bit from the neighbour unless coords are 0,0 (for even row and col)or 1,1 (for odd row and col)
    if( (this->row == 0 and this->col == 0)or(this->row == 1 and this->col == 1)){
        bool randomBit = generateStochasticBit(this->getParam<float>(CellRsdnf::PROBA),
                this->getParam<int>(CellRsdnf::PRECISION_PROBA));
        this->setRegState(RANDOM_OUT,randomBit);
    }else{
        this->setRegState(RANDOM_OUT,this->getNeighbour(this->neighbours.size()-1).get()->getRegState(RANDOM_OUT));
    }


}


void  RouterSequenceShortMixte::computeState(){

    int buffer = this->getRegState(BUFFER);
    int nbInput = 0;

    for(unsigned int i = 1 ; i < this->neighbours.size()-1;i++){ //-1 because the last neighbour is one giving the next random bit
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

    //update the random bit from the neighbour unless coords are 0,0
    if( (this->row == 0 and (this->dir == NeumannConnecter::E or this->dir == NeumannConnecter::W)) 
            or (this->col == 0 and(this->dir == NeumannConnecter::N or this-> dir == NeumannConnecter::S)) ){
        bool randomBit = generateStochasticBit(this->getParam<float>(CellRsdnf::PROBA),
                this->getParam<int>(CellRsdnf::PRECISION_PROBA));
        this->setRegState(RANDOM_OUT,randomBit);
    }else{
        this->setRegState(RANDOM_OUT,this->getNeighbour(this->neighbours.size()-1).get()->getRegState(RANDOM_OUT));
    }


}
