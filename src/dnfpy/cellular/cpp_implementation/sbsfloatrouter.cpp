#include "sbsfloatrouter.h"
#include "bitstreamfloatgenerator.h"
#include"cellsbsfloat.h"

SBSFloatRouter::SBSFloatRouter(int row,int col):BitStreamFloatGenerator(row,col)
{
    this->sbs.reset();
    this->synSBS.reset();
}


void SBSFloatRouter::reset(){
   BitStreamFloatGenerator::reset();
   this->sbs.reset();
   this->synSBS.reset();
}

void SBSFloatRouter::setDefaultParams(Module::ParamsPtr params){
    params->push_back(new int(20));//SIZE_STREAM
}

void SBSFloatRouter::setSynSBS(BitStreamFloat::BSFPtr sbs){
    this->synSBS = sbs;
}


BitStreamFloat::BSFPtr SBSFloatRouter::getSBS(){
    if (this->sbs){
        return this->sbs;
    }else{
        //std::cout << "getSBSRouter : " << std::endl;
        int sizeStream = this->getParam<int>(SBSFloatRouter::SIZE_STREAM);
        this->sbs = BitStreamFloat::BSFPtr(new BitStreamFloat(sizeStream));
        int i = 0;
        for(ModulePtr pred : this->neighbours){
            //std::cout << "sbs: " << *this->sbs << std::endl;
            //std::cout << "pred : " << ((BitStreamGenerator*)pred.get()) << std::endl;
            *(this->sbs) |= *(((BitStreamFloatGenerator*)pred.get())->getSBS());
            //std::cout << "pred : " << i << " : "<< this->sbs->count_ones() << std::endl;
            i++;
        }
        //std::cout << "synSBS : " << i << " : "<< synSBS->count_ones() << std::endl;
         *(this->sbs) &= *(this->synSBS);
        //std::cout << "set Router " << this->sbs->count_ones() << std::endl;
        return this->sbs;
    }
}
