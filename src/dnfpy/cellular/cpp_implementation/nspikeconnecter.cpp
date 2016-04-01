#include "nspikeconnecter.h"
#include "cellnspike.h"
/**
 * @brief NSpikeConnecter::cellConnection we add a cell n spike on the border to keep a constant number of neighbours
 * @param cell
 * @param neighCell
 * @param dir
 */
void NSpikeConnecter::cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const{
    if(neighCell!=nullptr){
        cell.get()->addNeighbour(neighCell);
    }else{
        Module::ModulePtr deadCell = Module::ModulePtr(new CellNSpike(-1,-1));
        ((CellNSpike*)deadCell.get())->setDead(true);
        cell.get()->addNeighbour(deadCell);
    }
}
