#include "cellrsdnf.h"
#include "router.h"
#include <iostream>

CellRsdnf::CellRsdnf() : Module()
{


    this->nbBitReceived = 0;
    this->activated = false;
    this->dead = false;
    this->initRouters();

   // std::cout << "constructing cellrsdnf " << std::endl;
}

void CellRsdnf::initRouters(){
    for(int i = 0 ; i < 4 ;i ++){
        Router* r = new Router();
        r->addNeighbour(this);
        this->subModules.push_back(r);
    }
}


void CellRsdnf::computeState(){
    int nbSpikeReceived = 0;
    for(Module* in:this->neighbours){
        nbSpikeReceived += in->getRegState<bool>(Router::SPIKE_OUT);
    }
//    if(nbSpikeReceived > 0){
//        std::cout << "nbSpikeReceived : " << nbSpikeReceived << std::endl;
//    }
    this->nbBitReceived += nbSpikeReceived;

    if(this->activated){
       // std::cout << "switch off activation" << std::endl;
        this->activated = false;
        for(Module* mod:this->subModules){
            Router* router = (Router*)mod;
            router->setActivated(false);
        }

    }
}


void CellRsdnf::getAttribute(int index,void* value){
    switch(index){
    case NB_BIT_RECEIVED:
        *((int*)value) = this->nbBitReceived;
        //std::cout << "val : "<< *((int*)value) << std::endl;
        return;
    case ACTIVATED:*((bool*)value) = this->activated;return;
    case DEAD:*((bool*)value) = this->dead;return;
    }
}


void CellRsdnf::setAttribute(int index, void* value){
    switch(index){
    case NB_BIT_RECEIVED:this->nbBitReceived = *((int*)value);return;
    case ACTIVATED:this->activated = *((bool*)value);
        for(Module* mod:this->subModules){
            Router* router = (Router*)mod;
            router->setActivated(this->activated);
        }
        return;
    case DEAD:this->dead=*((bool*)value);return;
    }
}
