#include "sbsfastrouter.h"
#include "bitstreamgenerator.h"
#include"cellsbsfast.h"

SBSFastRouter::SBSFastRouter()
{
    this->sbs.reset();
    this->synSBS.reset();
}


void SBSFastRouter::reset(){
   BitStreamGenerator::reset();
   this->sbs.reset();
   this->synSBS.reset();
}

void SBSFastRouter::setSynSBS(BitStreamUint::BSBPtr sbs){
    this->synSBS = sbs;
}


BitStreamUint::BSBPtr SBSFastRouter::getSBS(){
    //std::cout << "getSBSRouter : " << std::endl;
    if (this->sbs){
        return this->sbs;
    }else{
        int sizeStream = this->getParam<int>(CellSBSFast::SIZE_STREAM);
        this->sbs = BitStreamUint::BSBPtr(new BitStreamUint(sizeStream));
        int i = 0;
        for(ModulePtr pred : this->neighbours){
            //std::cout << "sbs: " << *this->sbs << std::endl;
           // std::cout << "pred : " << ((BitStreamGenerator*)pred.get()) << std::endl;
            *(this->sbs) |= *(((BitStreamGenerator*)pred.get())->getSBS());
            //std::cout << "pred : " << i << " : "<< this->sbs->count_ones() << std::endl;
            i++;
        }
       // std::cout << "synSBS : " << i << " : "<< synSBS.count_ones() << std::endl;
         *(this->sbs) &= *(this->synSBS);
        //std::cout << "set Router " << this->sbs->count_ones() << std::endl;
        return this->sbs;
    }
}
