#include "cellrsdnf.h"
#include "router.h"
#include "routerSequence.h"
#include "routerSequenceMixte.h"
#include "routerBit.h"
#include <iostream>
#include "bitstreamutils.h"

CellRsdnf::CellRsdnf(int row,int col,std::string typeRouter) : Module(row,col)
{


    //registres
    this->regs.push_back(Register(false,1));//ACTIVATED
    this->regs.push_back(Register(0,10));//NB_BIT_RECEIVED

    this->initRouters(typeRouter);

   // std::cout << "constructing cellrsdnf " << std::endl;
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
        r->initParams();//TODO this is a massive gotcha
    }
}

void CellRsdnf::setDefaultParams(Module::ParamsPtr params){

    params->push_back(new int(20));//NB_SPIKE

}


void CellRsdnf::computeState(){
    int nbSpikeReceived = 0;
    for(unsigned int i = 0 ; i < this->neighbours.size() ; i++){
        nbSpikeReceived += this->neighbours[i].get()->getRegState(Router::SPIKE_OUT);
    }

    this->setRegState(NB_BIT_RECEIVED,this->getRegState(NB_BIT_RECEIVED) + nbSpikeReceived);
//    if(nbSpikeReceived > 0){
//        std::cout << "nbSpikeReceived : " << nbSpikeReceived << std::endl;
//    }

    if(this->getRegState(ACTIVATED)){
       // std::cout << "switch off activation" << std::endl;
        for(ModulePtr mod:this->subModules){
            Router* r = ((Router*)mod.get());
            r->setRegState(Router::BUFFER,r->getRegState(Router::BUFFER)+this->getParam<int>(NB_SPIKE));
        }

        this->setRegState(ACTIVATED,false);
    }
}
