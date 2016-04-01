#include "cellrsdnf.h"
#include "router.h"
#include "routerSequence.h"
#include "routerSequenceMixte.h"
#include "routerBit.h"
#include <iostream>
#include "bitstreamutils.h"

CellRsdnf::CellRsdnf(int row,int col,std::string typeRouter) : Module(row,col)
{


    this->nbBitReceived = 0;
    this->activated = false;
    this->dead = false;
    this->initRouters(typeRouter);

   // std::cout << "constructing cellrsdnf " << std::endl;
}


void CellRsdnf::reset(){
    Module::reset();
    //reset atribbutes as well
    this->nbBitReceived = 0;
    this->activated = false;
    this->dead = false;

}

void CellRsdnf::initRouters(std::string typeRouter){

    for(int i = 0 ; i < 4 ;i ++){
        ModulePtr r= NULL;
        if(typeRouter.compare("prng") == 0){
            r = ModulePtr(new Router(this->row,this->col));
        }else if(typeRouter.compare("sequence") == 0){
            r = ModulePtr(new RouterSequence(this->row,this->col));
        }else if(typeRouter.compare("sequenceShort") == 0){
            r = ModulePtr(new RouterSequence(this->row,this->col));
        }else if(typeRouter.compare("sequenceMixte") == 0){
            r = ModulePtr(new RouterSequenceMixte(this->row,this->col));
        }else if(typeRouter.compare("sequenceShortMixte") == 0){
            r = ModulePtr(new RouterSequenceShortMixte(this->row,this->col,i));
        }else if(typeRouter.compare("bit") == 0){
            r = ModulePtr(new RouterBit(this->row,this->col));
        }else{
            std::cout << "invalid router name "<< typeRouter << std::endl;
            exit(-1);
        }


        this->subModules.push_back(r);
    }
}

void CellRsdnf::setDefaultParams(Module::ParamsPtr params){

    params->push_back(new int(20));//NB_SPIKE
    params->push_back(new float(1.0));//PROBA
    params->push_back(new long int(PRECISION_MAX));//PRECISION_PROBA

}


void CellRsdnf::computeState(){
    int nbSpikeReceived = 0;
    for(unsigned int i = 0 ; i < this->neighbours.size() ; i++){
        nbSpikeReceived += this->neighbours[i].get()->getRegState(Router::SPIKE_OUT);
    }

//    if(nbSpikeReceived > 0){
//        std::cout << "nbSpikeReceived : " << nbSpikeReceived << std::endl;
//    }
    this->nbBitReceived += nbSpikeReceived;

    if(this->activated){
       // std::cout << "switch off activation" << std::endl;
        this->activated = false;
        for(ModulePtr mod:this->subModules){
         ((Router*)mod.get())->setActivated(false);
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
        for(ModulePtr mod:this->subModules){
            ((Router*)mod.get())->setActivated(this->activated);
        }
        return;
    case DEAD:this->dead=*((bool*)value);return;
    }
}
