#include "router.h"
#include <iostream>
#include "param.h"
#include "bitstreamutils.h"

Router::Router(int row,int col) : Module(row,col)
{
    this->regs.push_back(Register(0));//BUFFER
    this->regs.push_back(Register(false));//SPIKE_OUT
}

void Router::setDefaultParams(Module::ParamsPtr params){
    params->push_back(new float(1.0));//PROBA
    params->push_back(new long int(PRECISION_MAX));//PRECISION_PROBA
}


bool Router::bernouilliTrial(float proba,int precision_proba){
    return generateStochasticBit(proba,precision_proba);
}

void Router::computeState(){
    int buffer = this->getRegState(BUFFER);
    int nbInput = 0;
    for(unsigned int i = 1 ; i < this->neighbours.size();i++){//first neigh is this neuron the other are predecessors in spike routing graph
        nbInput += this->getNeighbour(i).get()->getRegState(SPIKE_OUT);
    }

    if(buffer > 0 || nbInput > 0){
        if(this->bernouilliTrial(this->getParam<float>(PROBA),this->getParam<int>(PRECISION_PROBA))){
            this->setRegState(SPIKE_OUT,true);
        }else{
            this->setRegState(SPIKE_OUT,false);
        }
        buffer += nbInput-1;
        this->setRegState(BUFFER,buffer);
    }else{
        this->setRegState(SPIKE_OUT,false);
    }


}
