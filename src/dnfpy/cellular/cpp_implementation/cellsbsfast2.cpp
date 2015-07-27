#include "cellsbsfast2.h"
#include "sbsfastrouter.h"
CellSBSFast2::CellSBSFast2() : CellSBSFast()
{
    //Create 4 more routers for inhibitory layer
    for(unsigned int i = 0 ; i < 4 ;++i){
        ModulePtr router =  ModulePtr(new SBSFastRouter());
        this->subModules.push_back(router);
    }

   // std::cout << "nb router : " << this->subModules.size() << std::endl;

    this->nbInhBitReceived = 0;

}

void CellSBSFast2::setDefaultParams(ParamsPtr params){
    CellSBSFast::setDefaultParams(params);
    params->push_back(new float(1));//PROBA_SYNAPSE_INH
    params->push_back(new unsigned int(5)); //SHIFT
    params->push_back(new unsigned int(31)); //NB_SHARED_BIT
}

void CellSBSFast2::reset(){
    CellSBSFast::reset();
    this->nbInhBitReceived = 0;
}

void CellSBSFast2::computeState(){
    int sizeStream = this->getParam<int>(CellSBSFast_Parameters::SIZE_STREAM);
    BitStreamUint bsSumExc = BitStreamUint(sizeStream);
    BitStreamUint bsSumInh = BitStreamUint(sizeStream);
    unsigned int i;
    ModulePtr modExc,modInh;
    //std::cout << "nb neigh : " << this->neighbours.size() << std::endl;
    for(i = 0; i < this->neighbours.size() ; i+=2){
        modExc = this->neighbours[i];
        bsSumExc |= *(((BitStreamGenerator*)modExc.get())->getSBS());
        modInh = this->neighbours[i+1];
        bsSumInh |= *(((BitStreamGenerator*)modInh.get())->getSBS());
    }
    this->nbBitReceived = bsSumExc.count_ones();
    this->nbInhBitReceived = bsSumInh.count_ones();
    //std::cout << "nbReceived Cell : " << this->nbBitReceived << std::endl;
}

/**
 * @brief CellSBSFast::preCompute assume that  params are set
 */
void CellSBSFast2::preCompute(){
    int sizeStream = this->getParam<int>(CellSBSFast_Parameters::SIZE_STREAM);
    float probaSynapseExc = this->getParam<float>(CellSBSFast::PROBA_SYNAPSE);
    float probaSynapseInh = this->getParam<float>(CellSBSFast2::PROBA_SYNAPSE_INH);
    unsigned long int precisionMask = this->getParam<uint32_t>(CellSBSFast::PRECISION_PROBA);
    unsigned int shift = this->getParam<unsigned int>(CellSBSFast2::SHIFT);
    unsigned int nbSharedBit = this->getParam<unsigned int>(CellSBSFast2::NB_SHARED_BIT);

//    std::cout << "precision Proba : " << precisionMask << std::endl;
//    std::cout << "sizeStream : " << sizeStream << std::endl;
//    std::cout << "pExc : " << probaSynapseExc << std::endl;
//    std::cout << "pInh : " << probaSynapseInh << std::endl;

    std::vector<float> probaVec(8);
    for(unsigned int i = 0 ;i < 4 ; i++){
        probaVec[i] = probaSynapseExc;
    }
    for(unsigned int i = 4 ;i < 8 ; i++){
        probaVec[i] = probaSynapseInh;
    }
    if(this->activated){
        float probaSpike= this->getParam<float>(CellSBSFast_Parameters::PROBA_SPIKE);
        probaVec.push_back(probaSpike);
    }

    std::vector<BitStreamUint::BSBPtr> sbsVec = genRotatedSBS(probaVec.size(),probaVec,sizeStream,shift,nbSharedBit,precisionMask);

    //Init routers synaptic SBS
    ModulePtr mod;
    for(unsigned i = 0 ; i < 8 ; ++i){
        mod = this->subModules[i];
        //BitStreamUint::BSBPtr synSBSExc = BitStreamUint::BSBPtr( new BitStreamUint(probaSynapseExc,sizeStream,precisionMask));
        //BitStreamUint::BSBPtr synSBSInh = BitStreamUint::BSBPtr( new BitStreamUint(probaSynapseInh,sizeStream,precisionMask));
        ((SBSFastRouter*)mod.get())->setSynSBS(sbsVec[i]);
        //std::cout << "SBSExc : " << synSBSExc->mean() << std::endl;
    }

    //Init this Spike SBS
    if(this->activated){
        this->sbs = sbsVec[8];
    }else{
        this->sbs = BitStreamUint::BSBPtr(new BitStreamUint(sizeStream));
    }
    //std::cout << "SpikeSBS : " << this->sbs->mean() << std::endl;
}



void CellSBSFast2::getAttribute(int index,void* value){
    if(index < 3){
        CellSBSFast::getAttribute(index,value);
    }else if(index == NB_BIT_INH_RECEIVED){
         *((int*)value) = this->nbInhBitReceived;
    }else{
       throw "Attribute does not exist";
    }
}


void CellSBSFast2::setAttribute(int index, void* value){
    if(index < 3){
        CellSBSFast::setAttribute(index,value);
    }else if(index == NB_BIT_INH_RECEIVED){
          this->nbInhBitReceived = *((int*)value);
    }else{
       throw "Attribute does not exist";
    }
}

