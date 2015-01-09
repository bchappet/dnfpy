#include "cellbsrsdnf.h"
#include "bsrouter.h"
#include "bitstreamutils.h"
#include <iostream>

CellBsRsdnf::CellBsRsdnf() :Module(){

    for(int i = 0 ; i < 4 ;i ++){
        BSRouter* r = new BSRouter();
        r->addNeighbour(this);
        this->subModules.push_back(r);
    }
    //attributes
    this->nbBitReceived = 0;
    this->activated = false;
    this->dead = false;
    this->nbBitToGenerate = 0;
    //params:
    this->params.push_back(new Param<float>(1));//PROBA_SPIKE
    this->params.push_back(new Param<int>(20));//SIZE_STREAM
    this->params.push_back(new Param<float>(1.));//PROBA_SYNAPSE
    //link to submodule hence if we change this PROBA_SYNAPSE param it will change all sub mods
    for(Module* mod : this->subModules){
        this->linkParam(CellBsRsdnf_Parameters::PROBA_SYNAPSE,BSRouter::PROBA_SYNAPSE,mod);
    }
    //registres
    this->regs.push_back(new Register<bool>(0));//SPIKE_BS
}



void CellBsRsdnf::computeState(){
    int nbSpikeReceived = 0;
    bool ret = false;
    for(Module* in:this->neighbours){
        nbSpikeReceived += in->getRegState<bool>(BSRouter::BS_OUT);
        //std::cout << "nb spike received " << nbSpikeReceived << std::endl;
    }
    this->nbBitReceived += nbSpikeReceived;

    if(this->activated){
        this->nbBitToGenerate = this->getParam<int>(CellBsRsdnf_Parameters::SIZE_STREAM);
        this->activated = 0;
    }

    if(this->nbBitToGenerate > 0){
        ret = generateStochasticBit(this->getParam<float>(CellBsRsdnf_Parameters::PROBA_SPIKE));
        //std::cout << "bit to generate : " << this->nbBitToGenerate  <<  std::endl;
        this->nbBitToGenerate --;
    }
    this->setRegState<bool>(CellBsRsdnf_Registers::SPIKE_BS,ret);

}

void CellBsRsdnf::getAttribute(int index,void* value){
    switch(index){
    case NB_BIT_RECEIVED:
        *((int*)value) = this->nbBitReceived;return;
    case ACTIVATED:*((bool*)value) = this->activated;return;
    case DEAD:*((bool*)value) = this->dead;return;
    }
}


void CellBsRsdnf::setAttribute(int index, void* value){
    switch(index){
    case NB_BIT_RECEIVED:this->nbBitReceived = *((int*)value);return;
    case ACTIVATED:this->activated = *((bool*)value);return;
    case DEAD:this->dead=*((bool*)value);return;
    }
}
