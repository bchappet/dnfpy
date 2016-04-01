#include "cellsbsfast.h"
#include "bitstreamutils.h"
#include "sbsfastrouter.h"


CellSBSFast::CellSBSFast(int row,int col) : BitStreamGenerator(row,col)
{
    //Create routers
    for(int i = 0 ; i < 4 ;i ++){
        ModulePtr router =  ModulePtr(new SBSFastRouter(row,col));
        this->subModules.push_back(router);
    }

    //attributes
    this->nbBitReceived = 0;
    this->activated = false;
    this->dead = false;
    this->sbs.reset();
}

void CellSBSFast::setDefaultParams(ParamsPtr params){
    params->push_back(new float(1));//PROBA_SPIKE
    params->push_back(new int(20));//SIZE_STREAM
    params->push_back(new float(1.));//PROBA_SYNAPSE
    params->push_back(new unsigned long int(PRECISION_MAX));//PRECISION_PROBA
}

/**
 * @brief CellSBSFast::preCompute assume that  params are set
 */
void CellSBSFast::preCompute(){
    int sizeStream = this->getParam<int>(CellSBSFast_Parameters::SIZE_STREAM);
    float probaSynapse = this->getParam<float>(CellSBSFast::PROBA_SYNAPSE);
    unsigned long int precisionMask = this->getParam<unsigned long int>(CellSBSFast::PRECISION_PROBA);

    //Init routers synaptic SBS
    for(ModulePtr router:this->subModules){
        BitStreamUint::BSBPtr synSBS = BitStreamUint::BSBPtr( new BitStreamUint(probaSynapse,sizeStream,precisionMask));
        ((SBSFastRouter*)router.get())->setSynSBS(synSBS);
    }

    //Init this Spike SBS
    if(this->activated){
        float probaSpike= this->getParam<float>(CellSBSFast_Parameters::PROBA_SPIKE);
        this->sbs = BitStreamUint::BSBPtr(new BitStreamUint(probaSpike,sizeStream,precisionMask));
    }else{
        this->sbs = BitStreamUint::BSBPtr(new BitStreamUint(sizeStream));
    }
}

void CellSBSFast::reset(){
    BitStreamGenerator::reset();
    this->nbBitReceived = 0;
    this->activated = false;
    this->sbs.reset();
}

void CellSBSFast::computeState(){
    int sizeStream = this->getParam<int>(CellSBSFast_Parameters::SIZE_STREAM);
    BitStreamUint bsSum = BitStreamUint(sizeStream);
    for(ModulePtr mod : this->neighbours){
        bsSum |= *(((BitStreamGenerator*)mod.get())->getSBS());
    }
    this->nbBitReceived = bsSum.count_ones();
    //std::cout << "nbReceived Cell : " << this->nbBitReceived << std::endl;
}

BitStreamUint::BSBPtr CellSBSFast::getSBS(){
    return this->sbs;
}

void CellSBSFast::getAttribute(int index,void* value){
    switch(index){
    case NB_BIT_RECEIVED:
        *((int*)value) = this->nbBitReceived;return;
    case ACTIVATED:*((bool*)value) = this->activated;return;
    case DEAD:*((bool*)value) = this->dead;return;
    }
}


void CellSBSFast::setAttribute(int index, void* value){
    switch(index){
    case NB_BIT_RECEIVED:{
        this->nbBitReceived = *((int*)value);return;
    }break;
    case ACTIVATED:{ //init SBS
        this->activated = *((bool*)value);return;}break;
    case DEAD:{this->dead=*((bool*)value);return;}break;
    }
}




