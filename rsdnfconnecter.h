#ifndef RSDNFCONNECTER_H
#define RSDNFCONNECTER_H
#include "neumannconnecter.h"

class RsdnfConnecter:public NeumannConnecter
{
public:

    virtual void cellConnection(Module* cell,Module* neighCell,int dir)const override;

};

#endif // RSDNFCONNECTER_H
