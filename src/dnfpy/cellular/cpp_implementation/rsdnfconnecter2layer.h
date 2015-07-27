#ifndef RSDNFCONNECTER2LAYER_H
#define RSDNFCONNECTER2LAYER_H
#include "rsdnfconnecter.h"

class RsdnfConnecter2layer : public RsdnfConnecter
{
public:


    virtual void cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const override;

};

#endif // RSDNFCONNECTER2LAYER_H
