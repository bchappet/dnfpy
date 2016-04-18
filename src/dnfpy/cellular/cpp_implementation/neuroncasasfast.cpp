#include "neuroncasasfast.h"
#include "bitstreamutils.h"
#include "sbsfastrouter.h"


NeuronCasasFast::NeuronCasasFast(int row,int col) : BitStreamGenerator(row,col)
{
    //Create routers
    for(int i = 0 ; i < 8 ;i ++){
        ModulePtr router =  ModulePtr(new SBSFastRouter(row,col));
        this->subModules.push_back(router);
        router->initParams();//TODO this is a massive gotcha
    }

    //attributes
    this->stim = 0;
    this->nbBitExc = 0;
    this->nbBitInh = 0;
    this->nbBitStim = 0;
    this->nbBitAct = 0;
    this->sbs.reset(new BitStreamUint(1000));
    this->potentialSbs.reset(new BitStreamUint(0.5f,1000));//bipolar bs
}

void NeuronCasasFast::setDefaultParams(ParamsPtr params){
    params->push_back(new int(1000));//SIZE_POTENTIAL_STREAM
    params->push_back(new int(25));//THRESHOLD
    params->push_back(new float(1.));//PROBA_EXC
    params->push_back(new float(1.));//PROBA_INH
    params->push_back(new unsigned long int(PRECISION_MAX));//PRECISION_PROBA
    params->push_back(new float(1.));//TAU
}

void NeuronCasasFast::reset(){
    BitStreamGenerator::reset();
    this->stim = 0;
    this->nbBitExc = 0;
    this->nbBitInh = 0;
    this->nbBitStim = 0;
    this->nbBitAct = 0;
    int sizeStream = this->getParam<int>(SIZE_POTENTIAL_STREAM);
    this->sbs.reset(new BitStreamUint(sizeStream));
    //TODO for now the size of potential SBS is changing only on reset
    this->potentialSbs.reset(new BitStreamUint(0.5f,sizeStream));//bipolar bs
}


/**
 * @brief NeuronCasasFast::preCompute assume that  params are set
 */
void NeuronCasasFast::preCompute(){
    int sizeStream = this->getParam<int>(SIZE_POTENTIAL_STREAM);
    unsigned long int precisionMask = this->getParam<unsigned long int>(PRECISION_PROBA);
    float probaExc = this->getParam<float>(PROBA_EXC);
    float probaInh = this->getParam<float>(PROBA_INH);

    //Init routers synaptic SBS
    for(unsigned int i = 0; i < 8 ; ++i){
        ModulePtr router = this->subModules[i];
        router->reset();//reset sbs of router or they dont recompute it
        float proba = i < 4 ? probaExc : probaInh;
        BitStreamUint::BSBPtr synSBS = BitStreamUint::BSBPtr( new BitStreamUint(proba,sizeStream,precisionMask));
        ((SBSFastRouter*)router.get())->setSynSBS(synSBS);
    }


    
}

void NeuronCasasFast::computeState(){
    //Sumation of laeral streams like in SBSFast2
    int sizeStream = this->getParam<int>(SIZE_POTENTIAL_STREAM);
    float tau = this->getParam<float>(TAU);
    BitStreamUint bsSumExc = BitStreamUint(sizeStream);
    BitStreamUint bsSumInh = BitStreamUint(sizeStream);
    for(unsigned int i = 0; i < this->neighbours.size() ; i+=2){
        ModulePtr mod = this->getNeighbour(i);
        bsSumExc |= *(((BitStreamGenerator*)mod.get())->getSBS());

        mod = this->getNeighbour(i+1);
        bsSumInh |= *(((BitStreamGenerator*)mod.get())->getSBS());
    }
    this->nbBitExc = bsSumExc.count_ones();
    this->nbBitInh = bsSumInh.count_ones();


    //for now we generate stimulu from attributes
    BitStreamUint bsStim = BitStreamUint(stim,sizeStream);
    //std::cout << "stim: " << stim << std::endl;

    //Update of the potential SBS
    BitStreamUint pot = *(this->potentialSbs.get());
    BitStreamUint lat =   ((pot | bsSumExc) & ~(bsSumInh)) | bsStim;
    BitStreamUint tauSB = BitStreamUint(tau,sizeStream);
    BitStreamUint leak = pot ^ tauSB; 
    this->potentialSbs.get()->copy (lat + leak);

    //Compute activation bit stream
    int threshold = this->getParam<int>(THRESHOLD);
    //TODO not really a counter but more like a threshold in tis implemetntation
    this->sbs->copy(this->potentialSbs->applyCounter(threshold,sizeStream));
    this->nbBitAct = this->sbs->count_ones();
    if(this->nbBitAct > 0){
        std::cout << this << std::endl;
        std::cout << "th " << threshold << std::endl;
        std::cout << "act " << this->nbBitAct << std::endl;
    }
    //TODO we should reset potential as well



}

BitStreamUint::BSBPtr NeuronCasasFast::getSBS(){
    //int count = this->sbs->count_ones() ;
    //if(true){
    //    std::cout << this << std::endl;
    //    std::cout << "SPIKE SBS:: " << this->sbs->count_ones() << std::endl;
    //}
    return this->sbs;
}

BitStreamUint::BSBPtr NeuronCasasFast::getPotSBS(){
    return this->potentialSbs;
}

void NeuronCasasFast::getAttribute(int index,void* value){
    switch(index){
    case POTENTIAL:
        *((float*)value) = this->potentialSbs.get()->mean();return;
    case NB_ACT:
        *((int*)value) = this->nbBitAct;return;
    case STIM:
        *((float*)value) = this->stim;return;
    case NB_BIT_EXC:
        *((int*)value) = this->nbBitExc;return;
    case NB_BIT_INH:
        *((int*)value) = this->nbBitInh;return;
    case NB_BIT_STIM:
        *((int*)value) = this->nbBitStim;return;
    }
}


void NeuronCasasFast::setAttribute(int index, void* value){
    switch(index){
    case STIM:
     this->stim =    *((float*)value) ;
        return;
    }
}




