#include "cellrsdnf.h"
#include "router.h"
#include <iostream>

CellRsdnf::CellRsdnf() : Module()
{

    for(int i = 0 ; i < 4 ;i ++){
        Router* r = new Router();
        r->addNeighbour(this); //SPIKE_OUT
        this->subModules.push_back(r);
    }
    this->regs.push_back(new Register<int>(0)); //POTNETIEL
    this->regs.push_back(new Register<bool>(false)); //activated_out

   // std::cout << "constructing cellrsdnf " << std::endl;
}

void CellRsdnf::computeState(){
    int nbSpikeReceived = 0;
    for(Module* in:this->neighbours){
        nbSpikeReceived += in->getRegState<bool>(Router::SPIKE_OUT);
    }
//    if(nbSpikeReceived > 0){
//        std::cout << "nbSpikeReceived : " << nbSpikeReceived << std::endl;
//    }
    this->setRegState<int>(POTENTIAL,this->getRegState<int>(POTENTIAL)+nbSpikeReceived);

    if(this->getRegState<bool>(ACTIVATED_OUT)){
       // std::cout << "switch off activation" << std::endl;
        this->setRegState<bool>(ACTIVATED_OUT,false);
    }
}
