#include "rsdnfconnecter.h"

void RsdnfConnecter::cellConnection(Module::ModulePtr cell)const {
    for(Module::ModulePtr mod :cell->getSubModules()){
        mod->addNeighbour(cell);//the first neighbour is the cell
    }
}

void RsdnfConnecter::cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const{
    if(neighCell != nullptr){
        switch(dir){
        case N:
            cell->addNeighbour(neighCell.get()->getSubModule(S));//we need it for potential computation
            cell->getSubModule(S).get()->addNeighbour(neighCell.get()->getSubModule(S));
            cell->getSubModule(E).get()->addNeighbour(neighCell.get()->getSubModule(S));
            cell->getSubModule(W).get()->addNeighbour(neighCell.get()->getSubModule(S));
            break;
        case S:
            cell->addNeighbour(neighCell.get()->getSubModule(N));//we need it for potential computation
            cell->getSubModule(N).get()->addNeighbour(neighCell.get()->getSubModule(N));
            cell->getSubModule(E).get()->addNeighbour(neighCell.get()->getSubModule(N));
            cell->getSubModule(W).get()->addNeighbour(neighCell.get()->getSubModule(N));
            break;
        case E:
            cell->addNeighbour(neighCell.get()->getSubModule(W));//we need it for potential computation
            cell->getSubModule(W).get()->addNeighbour(neighCell.get()->getSubModule(W));
            break;
        case W:
            cell->addNeighbour(neighCell.get()->getSubModule(E));//we need it for potential computation
            cell->getSubModule(E).get()->addNeighbour(neighCell.get()->getSubModule(E));
            break;
        }
    }
}
