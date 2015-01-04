#ifndef RSDNFCONNECTER_H
#define RSDNFCONNECTER_H
#include "neumannconnecter.h"
#include "cellrsdnf.h"
class RsdnfConnecter:public NeumannConnecter
{
public:
    RsdnfConnecter(){}
    virtual void cellConnection(Module* cell,Module* neighCell,int dir)const override{
        if(neighCell != nullptr){
            switch(dir){
            case N:
                cell->addInput(neighCell->getSubModule(S));//we need it for potential computation
                cell->getSubModule(S)->addInput(neighCell->getSubModule(S));
                cell->getSubModule(E)->addInput(neighCell->getSubModule(S));
                cell->getSubModule(W)->addInput(neighCell->getSubModule(S));
                break;
            case S:
                cell->addInput(neighCell->getSubModule(N));//we need it for potential computation
                cell->getSubModule(N)->addInput(neighCell->getSubModule(N));
                cell->getSubModule(E)->addInput(neighCell->getSubModule(N));
                cell->getSubModule(W)->addInput(neighCell->getSubModule(N));
                break;
            case E:
                cell->addInput(neighCell->getSubModule(W));//we need it for potential computation
                cell->getSubModule(W)->addInput(neighCell->getSubModule(W));
                break;
            case W:
                cell->addInput(neighCell->getSubModule(E));//we need it for potential computation
                cell->getSubModule(E)->addInput(neighCell->getSubModule(E));
                break;
            }
        }
    }

};

#endif // RSDNFCONNECTER_H
