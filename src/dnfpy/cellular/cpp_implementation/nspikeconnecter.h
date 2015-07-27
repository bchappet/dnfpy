#ifndef NSPIKECONNECTER_H
#define NSPIKECONNECTER_H
#include "neumannconnecter.h"
class NSpikeConnecter : public NeumannConnecter
{
public:
    virtual void cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const override;
};

#endif // NSPIKECONNECTER_H
