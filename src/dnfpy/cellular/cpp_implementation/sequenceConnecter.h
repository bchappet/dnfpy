#ifndef SEQUENCECONNECTER_H
#define SEQUENCECONNECTER_H
#include "neumannconnecter.h"
/**
 * Opposite connection to RSDNF to avoid any correlation with spike propagation
 * 12 linked to 1
 */
class SequenceConnecter:public NeumannConnecter
{
public:

    virtual void cellConnection(Module::ModulePtr cell)const override;
    virtual void cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const override;


};

#endif // SEQUENCECONNECTER_H
