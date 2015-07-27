#include "rsdnfconnecter2layer.h"
#define NB_ROUTER 4
void RsdnfConnecter2layer::cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const{
    if(neighCell != nullptr){

        switch(dir){
        case N:
            cell->addNeighbour(neighCell->getSubModule(S));//we need it for potential computation
            cell->getSubModule(S)->addNeighbour(neighCell->getSubModule(S));
            cell->getSubModule(E)->addNeighbour(neighCell->getSubModule(S));
            cell->getSubModule(W)->addNeighbour(neighCell->getSubModule(S));

            //Second layer connections
            cell->addNeighbour(neighCell->getSubModule(S+NB_ROUTER));//we need it for potential computation
            cell->getSubModule(S+NB_ROUTER)->addNeighbour(neighCell->getSubModule(S+NB_ROUTER));
            cell->getSubModule(E+NB_ROUTER)->addNeighbour(neighCell->getSubModule(S+NB_ROUTER));
            cell->getSubModule(W+NB_ROUTER)->addNeighbour(neighCell->getSubModule(S+NB_ROUTER));
            break;
        case S:
            cell->addNeighbour(neighCell->getSubModule(N));//we need it for potential computation
            cell->getSubModule(N)->addNeighbour(neighCell->getSubModule(N));
            cell->getSubModule(E)->addNeighbour(neighCell->getSubModule(N));
            cell->getSubModule(W)->addNeighbour(neighCell->getSubModule(N));

            //Second layer connections
            cell->addNeighbour(neighCell->getSubModule(N+NB_ROUTER));//we need it for potential computation
            cell->getSubModule(N+NB_ROUTER)->addNeighbour(neighCell->getSubModule(N+NB_ROUTER));
            cell->getSubModule(E+NB_ROUTER)->addNeighbour(neighCell->getSubModule(N+NB_ROUTER));
            cell->getSubModule(W+NB_ROUTER)->addNeighbour(neighCell->getSubModule(N+NB_ROUTER));
            break;
        case E:
            cell->addNeighbour(neighCell->getSubModule(W));//we need it for potential computation
            cell->getSubModule(W)->addNeighbour(neighCell->getSubModule(W));

            //Second layer connections
            cell->addNeighbour(neighCell->getSubModule(W+NB_ROUTER));//we need it for potential computation
            cell->getSubModule(W+NB_ROUTER)->addNeighbour(neighCell->getSubModule(W+NB_ROUTER));
            break;
        case W:
            cell->addNeighbour(neighCell->getSubModule(E));//we need it for potential computation
            cell->getSubModule(E)->addNeighbour(neighCell->getSubModule(E));

            //Second layer connections
            cell->addNeighbour(neighCell->getSubModule(E+NB_ROUTER));//we need it for potential computation
            cell->getSubModule(E+NB_ROUTER)->addNeighbour(neighCell->getSubModule(E+NB_ROUTER));
            break;
        }
    }
}
