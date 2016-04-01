#include "cellrsdnf2.h"
#include "routerBit.h"
#include <iostream>
#include "bitstreamutils.h"

CellRsdnf2::CellRsdnf2(int row,int col): CellRsdnf(row,col,"bit")
{

    this->nbBitInhReceived = 0;

   // std::cout << "constructing cellrsdnf " << std::endl;
    //Create 4 more routers for inhibitory layer
    for(int i = 0 ; i < 4 ;i ++){
        ModulePtr r= NULL;
        r = ModulePtr(new RouterBit(this->row,this->col));
        this->subModules.push_back(r);
    }
}


void CellRsdnf2::reset(){
    CellRsdnf::reset();
    //reset atribbutes as well
    this->nbBitInhReceived = 0;
}



void CellRsdnf2::setDefaultParams(Module::ParamsPtr params){
    CellRsdnf::setDefaultParams(params);

    params->push_back(new float(1.0));//PROBA_SYNAPSE_INH
    params->push_back(new unsigned int(PRECISION_MAX)); //PRECISION_RANDOM
    params->push_back(new unsigned int(31)); //NB_BIT_PROBA
    params->push_back(new unsigned int(0)); //shift

}

/*
 * @brief CellSBSFast::preCompute assume that  params are set
 * We will set the random bits of the 8 routers
 */
void CellRsdnf2::preCompute(){
    float probaSynapseExc = this->getParam<float>(CellRsdnf::PROBA);
    float probaSynapseInh = this->getParam<float>(CellRsdnf2::PROBA_INH);
    unsigned long int probaPrecisionMask = this->getParam<uint32_t>(CellRsdnf::PRECISION_PROBA);
    unsigned long int randomBitPrecisionMask = this->getParam<uint32_t>(CellRsdnf2::PRECISION_RANDOM);
    unsigned int nbBitProba = this->getParam<unsigned int>(CellRsdnf2::NB_BIT_RANDOM);
    unsigned int shift = this->getParam<unsigned int>(CellRsdnf2::SHIFT);

    //we generate only one random integer at each iteration
    u_int32_t randInt = genRandInt(randomBitPrecisionMask);
    for(unsigned int i = 0 ; i < 8 ; ++i){
        u_int32_t rotatedRandomInt = rotl32( randInt, shift, nbBitProba,randomBitPrecisionMask);
        RouterBit* router = (RouterBit*)this->subModules[i].get();
        float proba;
        if( i < 4)
            proba = probaSynapseExc;
        else
            proba = probaSynapseInh;

        bool randBit = getRandBitFromRandInt(rotatedRandomInt,proba,probaPrecisionMask);
        router->setAttribute(RouterBit::RANDOM_BIT,&randBit);

    }
    


}

void CellRsdnf2::computeState(){
    int nbSpikeReceived = 0;
    int nbSpikeReceivedInh = 0;
    for(unsigned i = 0; i < this->neighbours.size() ; i+=2){
        nbSpikeReceived += this->neighbours[i].get()->getRegState(Router::SPIKE_OUT);
        nbSpikeReceivedInh += this->neighbours[i+1].get()->getRegState(Router::SPIKE_OUT);

    }

//    if(nbSpikeReceived > 0){
//        std::cout << "nbSpikeReceived : " << nbSpikeReceived << std::endl;
//    }
    this->nbBitReceived += nbSpikeReceived;
    this->nbBitInhReceived += nbSpikeReceivedInh;

    if(this->activated){
       // std::cout << "switch off activation" << std::endl;
        this->activated = false;
        for(ModulePtr mod:this->subModules){
         ((Router*)mod.get())->setActivated(false);
        }

    }
}


void CellRsdnf2::getAttribute(int index,void* value){
    switch(index){
    case NB_BIT_RECEIVED:
        *((int*)value) = this->nbBitReceived;
        //std::cout << "val : "<< *((int*)value) << std::endl;
        return;
    case ACTIVATED:*((bool*)value) = this->activated;return;
    case DEAD:*((bool*)value) = this->dead;return;
    case NB_BIT_INH_RECEIVED : 
        *((int*)value) = this->nbBitInhReceived;
        return;
    }
}


void CellRsdnf2::setAttribute(int index, void* value){
    switch(index){
    case NB_BIT_RECEIVED:this->nbBitReceived = *((int*)value);return;
    case ACTIVATED:this->activated = *((bool*)value);
        for(ModulePtr mod:this->subModules){
            ((Router*)mod.get())->setActivated(this->activated);
        }
        return;
    case DEAD:this->dead=*((bool*)value);return;
    case NB_BIT_INH_RECEIVED:this->nbBitInhReceived = *((int*)value);return;
    }
}
