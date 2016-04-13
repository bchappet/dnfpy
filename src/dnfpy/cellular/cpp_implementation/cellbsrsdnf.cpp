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

CellBsRsdnf::CellBsRsdnf(int row, int col,std::string typeRouter) :Module(row,col){

    //allocate the lastRandomNumber
    this->lastRandomNumber= new int;
    *this->lastRandomNumber = 0;


    for(int i = 0 ; i < 4 ;i ++){
        ModulePtr r = getRouter(typeRouter);
        this->subModules.push_back(r);
        r->initParams();//TODO this is a massive gotcha
    }

    //registres
    this->regs.push_back(Register(0,1));//SPIKE_BS
    this->regs.push_back(Register(0,10));//NB_BIT_RECEIVED
    this->regs.push_back(Register(0,1));//ACTIVATED
    this->regs.push_back(Register(0,10));//NB_BIT_TO_GEN


}


void CellBsRsdnf::setDefaultParams(ParamsPtr params){
    params->push_back(new float(1));//PROBA_SPIKE
    params->push_back(new int(20));//SIZE_STREAM
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

    this->incrReg(NB_BIT_RECEIVED,nbSpikeReceived);

    int nb_bit_to_gen = this->getRegState(NB_BIT_TO_GEN);

    if(this->getRegState(CellBsRsdnf::ACTIVATED)){
        //std::cout << "activated"<<std::endl;
        nb_bit_to_gen = this->getParam<int>(CellBsRsdnf_Parameters::SIZE_STREAM);
        //std::cout << "nb bit to generate : " << this->nbBitToGenerate << std::endl;
        this->setRegState(CellBsRsdnf::ACTIVATED,0);
    }

    if(this->getRegState(NB_BIT_TO_GEN) > 0 or this->getRegState(CellBsRsdnf::ACTIVATED)){
        //std::cout << "nb bit to gen " << this->getRegState(NB_BIT_TO_GEN) << std::endl; 
        ret = generateStochasticBit(this->getParam<float>(CellBsRsdnf::PROBA_SPIKE),
                                    this->getParam<int>(CellBsRsdnf::PRECISION_PROBA_SPIKE));
                                   // this->lastRandomNumber,
                                   // this->getParam<int>(CellBsRsdnf_Parameters::NB_NEW_RANDOM_BIT));
        //std::cout << "bit to generate : " << this->nbBitToGenerate  <<  std::endl;
        nb_bit_to_gen --;
    }
    this->setRegState(CellBsRsdnf_Registers::SPIKE_BS,ret);
    this->setRegState(NB_BIT_TO_GEN,nb_bit_to_gen);

}

