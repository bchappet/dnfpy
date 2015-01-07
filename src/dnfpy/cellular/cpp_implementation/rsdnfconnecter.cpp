#include "rsdnfconnecter.h"


void RsdnfConnecter::cellConnection(Module* cell,Module* neighCell,int dir)const{
    if(neighCell != nullptr){
        switch(dir){
        case N:
            cell->addNeighbour(neighCell->getSubModule(S));//we need it for potential computation
            cell->getSubModule(S)->addNeighbour(neighCell->getSubModule(S));
            cell->getSubModule(E)->addNeighbour(neighCell->getSubModule(S));
            cell->getSubModule(W)->addNeighbour(neighCell->getSubModule(S));
            break;
        case S:
            cell->addNeighbour(neighCell->getSubModule(N));//we need it for potential computation
            cell->getSubModule(N)->addNeighbour(neighCell->getSubModule(N));
            cell->getSubModule(E)->addNeighbour(neighCell->getSubModule(N));
            cell->getSubModule(W)->addNeighbour(neighCell->getSubModule(N));
            break;
        case E:
            cell->addNeighbour(neighCell->getSubModule(W));//we need it for potential computation
            cell->getSubModule(W)->addNeighbour(neighCell->getSubModule(W));
            break;
        case W:
            cell->addNeighbour(neighCell->getSubModule(E));//we need it for potential computation
            cell->getSubModule(E)->addNeighbour(neighCell->getSubModule(E));
            break;
        }
    }
}
