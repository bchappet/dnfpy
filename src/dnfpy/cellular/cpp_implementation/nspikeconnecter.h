#ifndef NSPIKECONNECTER_H
#define NSPIKECONNECTER_H
#include "neumannconnecter.h"
class NSpikeConnecter : public NeumannConnecter
{
public:
    virtual void cellConnection(Module* cell,Module* neighCell,int dir)const override;
};

#endif // NSPIKECONNECTER_H
