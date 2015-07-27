#include "cellbsrsdnf.h"
#include "bsrouter.h"
#include "carrybsrouter.h"
#include "bitstreamutils.h"
#include <iostream>


Module::ModulePtr getRouter(std::string typeRouter){
    Module::ModulePtr router;
    if(typeRouter.compare("carryRouter") == 0){
        router =  Module::ModulePtr(new CarryBsRouter());
    }else{ //(typeRouter.compare("orRouter") == 0){
        router =  Module::ModulePtr(new BSRouter());
    }
    return router;
}

CellBsRsdnf::~CellBsRsdnf(){
    delete this->lastRandomNumber;
}

CellBsRsdnf::CellBsRsdnf(std::string typeRouter) :Module(){

    //allocate the lastRandomNumber
    this->lastRandomNumber= new int;
    *this->lastRandomNumber = 0;


    for(int i = 0 ; i < 4 ;i ++){
        ModulePtr r = getRouter(typeRouter);
        this->subModules.push_back(r);
    }
    //attributes
    this->nbBitReceived = 0;
    this->activated = false;
    this->dead = false;
    this->nbBitToGenerate = 0;
    //params



    //registres
    this->regs.push_back(Register(0));//SPIKE_BS


}


void CellBsRsdnf::setDefaultParams(ParamsPtr params){
    params->push_back(new float(1));//PROBA_SPIKE
    params->push_back(new int(20));//SIZE_STREAM
    params->push_back(new float(1.));//PROBA_SYNAPSE
    params->push_back(new unsigned long int(PRECISION_MAX));//PRECISION_PROBA
    params->push_back(new int(30));//NB_NEW_RANDOM_BIT

}



void CellBsRsdnf::computeState(){
    int nbSpikeReceived = 0;
    bool ret = false;


    bool bsSum = false;
    for(ModulePtr in :this->neighbours){
        bsSum |= in->getRegState(BSRouter::BS_OUT);
        //std::cout << "nb spike received " << nbSpikeReceived << std::endl;
    }
    nbSpikeReceived = bsSum;//number spike received = 1 or 0

    this->nbBitReceived += nbSpikeReceived;

    if(this->activated){
        //std::cout << "activated"<<std::endl;
        this->nbBitToGenerate = this->getParam<int>(CellBsRsdnf_Parameters::SIZE_STREAM);
        //std::cout << "nb bit to generate : " << this->nbBitToGenerate << std::endl;
        this->activated = 0;
    }

    if(this->nbBitToGenerate > 0){
        ret = generateStochasticBit(this->getParam<float>(CellBsRsdnf_Parameters::PROBA_SPIKE),
                                    this->getParam<int>(CellBsRsdnf_Parameters::PRECISION_PROBA));
                                   // this->lastRandomNumber,
                                   // this->getParam<int>(CellBsRsdnf_Parameters::NB_NEW_RANDOM_BIT));
        //std::cout << "bit to generate : " << this->nbBitToGenerate  <<  std::endl;
        this->nbBitToGenerate --;
    }
    this->setRegState(CellBsRsdnf_Registers::SPIKE_BS,ret);

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
