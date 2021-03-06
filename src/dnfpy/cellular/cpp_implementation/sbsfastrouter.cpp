#include "sbsfastrouter.h"
#include "bitstreamgenerator.h"
#include"cellsbsfast.h"

SBSFastRouter::SBSFastRouter(int row,int col):BitStreamGenerator(row,col)
{
    this->sbs.reset();
    this->synSBS.reset();
}


void SBSFastRouter::reset(){
   BitStreamGenerator::reset();
   this->sbs.reset();
   this->synSBS.reset();
}

void SBSFastRouter::setDefaultParams(Module::ParamsPtr params){
    params->push_back(new int(20));//SIZE_STREAM
}

void SBSFastRouter::setSynSBS(BitStreamUint::BSBPtr sbs){
    this->synSBS = sbs;
}


BitStreamUint::BSBPtr SBSFastRouter::getSBS(){
    if (this->sbs){
        return this->sbs;
    }else{
        //std::cout << "getSBSRouter : " << std::endl;
        int sizeStream = this->getParam<int>(SBSFastRouter::SIZE_STREAM);
        this->sbs = BitStreamUint::BSBPtr(new BitStreamUint(sizeStream));
        int i = 0;
        for(ModulePtr pred : this->neighbours){
            //std::cout << "sbs: " << *this->sbs << std::endl;
            //std::cout << "pred : " << ((BitStreamGenerator*)pred.get()) << std::endl;
            *(this->sbs) |= *(((BitStreamGenerator*)pred.get())->getSBS());
            //std::cout << "pred : " << i << " : "<< this->sbs->count_ones() << std::endl;
            i++;
        }
        //std::cout << "synSBS : " << i << " : "<< synSBS->count_ones() << std::endl;
         *(this->sbs) &= *(this->synSBS);
        //std::cout << "set Router " << this->sbs->count_ones() << std::endl;
        return this->sbs;
    }
}
