#include "sequenceConnecter.h"

/**
 * For now only for rsdnfSequence router and rsdnf cell
 *
 */
void SequenceConnecter::cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell) const{
    unsigned int nbSubModule = cell->getSubModuleCount();
    for(unsigned int i = 0 ; i < nbSubModule; ++i){
        cell->getSubModule(i).get()->addNeighbour(neighCell.get()->getSubModule((i+1)%nbSubModule));
    }
}


void SequenceConnecter::connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray) const{
    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
            Module::ModulePtr cell = cellArray[i][j];
            
            if(i == 0 && j == 0){
                //the predecessor is the last cell
                this->cellNeighbourConnection(cell,cellArray[height-1][width-1]);
            }else{
                if(j == 0){
                    //the predecessor is the cell at the end of previous row 
                    //
                    this->cellNeighbourConnection(cell,cellArray[i-1][width-1]);
                }else{
                    //the predecessor is the previous cell on the same row
                    this->cellNeighbourConnection(cell,cellArray[i][j-1]);
                }

            }

        }
    }
}
