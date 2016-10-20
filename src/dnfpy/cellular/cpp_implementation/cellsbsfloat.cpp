#include "cellsbsfloat.h"
#include "bitstreamutils.h"
#include "sbsfloatrouter.h"


CellSBSFloat::CellSBSFloat(int row,int col) : BitStreamFloatGenerator(row,col)
{
    //Create routers
    for(int i = 0 ; i < 4 ;i ++){
        ModulePtr router =  ModulePtr(new SBSFloatRouter(row,col));
        this->subModules.push_back(router);
        router->initParams();//TODO this is a massive gotcha
    }

    //attributes
    this->value = 0.0f;
    this->activated = false;
    this->dead = false;
    this->sbs.reset();
}

void CellSBSFloat::setDefaultParams(ParamsPtr params){
    params->push_back(new float(1));//PROBA_SPIKE
    params->push_back(new int(20));//SIZE_STREAM
    params->push_back(new float(1.));//PROBA_SYNAPSE
    params->push_back(new unsigned long int(PRECISION_MAX));//PRECISION_PROBA
}

/**
 * @brief CellSBSFloat::preCompute assume that  params are set
 */
void CellSBSFloat::preCompute(){
    int sizeStream = this->getParam<int>(CellSBSFloat_Parameters::SIZE_STREAM);
    float probaSynapse = this->getParam<float>(CellSBSFloat::PROBA_SYNAPSE);
    unsigned long int precisionMask = this->getParam<unsigned long int>(CellSBSFloat::PRECISION_PROBA);

    //Init routers synaptic SBS
    for(ModulePtr router:this->subModules){
        BitStreamFloat::BSFPtr synSBS = 
            BitStreamFloat::BSFPtr( new BitStreamFloat(probaSynapse,sizeStream,precisionMask));
        ((SBSFloatRouter*)router.get())->setSynSBS(synSBS);
    }

    //Init this Spike SBS
    if(this->activated){
        float probaSpike= this->getParam<float>(CellSBSFloat_Parameters::PROBA_SPIKE);
        this->sbs = BitStreamFloat::BSFPtr(new BitStreamFloat(probaSpike,sizeStream,precisionMask));
    }else{
        //0 stream
        this->sbs = BitStreamFloat::BSFPtr(new BitStreamFloat(sizeStream));
    }
}

void CellSBSFloat::reset(){
    BitStreamFloatGenerator::reset();
    this->value = 0.0f;
    this->activated = false;
    this->sbs.reset();
}

void CellSBSFloat::computeState(){
    int sizeStream = this->getParam<int>(CellSBSFloat_Parameters::SIZE_STREAM);
    BitStreamFloat bsSum = BitStreamFloat(sizeStream);
    for(ModulePtr mod : this->neighbours){
        bsSum |= *(((BitStreamFloatGenerator*)mod.get())->getSBS());
    }
    this->value = bsSum.mean();
}

BitStreamFloat::BSFPtr CellSBSFloat::getSBS(){
    return this->sbs;
}

void CellSBSFloat::getAttribute(int index,void* value){
    switch(index){
    case VALUE:
        *((float*)value) = this->value;return;
    case ACTIVATED:*((bool*)value) = this->activated;return;
    case DEAD:*((bool*)value) = this->dead;return;
    }
}


void CellSBSFloat::setAttribute(int index, void* value){
    switch(index){
    case VALUE:{
        this->value = *((float*)value);return;
    }break;
    case ACTIVATED:{ //init SBS
        this->activated = *((bool*)value);return;}break;
    case DEAD:{this->dead=*((bool*)value);return;}break;
    }
}




