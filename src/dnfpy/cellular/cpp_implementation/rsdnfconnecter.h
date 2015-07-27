#ifndef RSDNFCONNECTER_H
#define RSDNFCONNECTER_H
#include "neumannconnecter.h"

class RsdnfConnecter:public NeumannConnecter
{
public:

    virtual void cellConnection(Module::ModulePtr cell)const override;

    virtual void cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const override;

};

#endif // RSDNFCONNECTER_H
