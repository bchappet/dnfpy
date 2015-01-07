#include "nspikeconnecter.h"
#include "cellnspike.h"
/**
 * @brief NSpikeConnecter::cellConnection we add a cell n spike on the border to keep a constant number of neighbours
 * @param cell
 * @param neighCell
 * @param dir
 */
void NSpikeConnecter::cellConnection(Module* cell,Module* neighCell,int dir)const{
    if(neighCell!=nullptr){
        cell->addNeighbour(neighCell);
    }else{
        CellNSpike* deadCell = new CellNSpike();
        deadCell->setDead(true);
        cell->addNeighbour(deadCell);
    }
}
