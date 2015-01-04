#ifndef ROUTER_H
#define ROUTER_H
#include "module.h"


class Router : public Module
{
public:
    enum RouterRegister { BUFFER,SPIKE_OUT} ;
    Router();
    virtual void computeState() override;
protected:
    const int NB_SPIKE = 20;
};

#endif // ROUTER_H
