#ifndef ROUTER_H
#define ROUTER_H
#include "module.h"


class Router : public Module
{
public:
    enum RouterRegister { BUFFER,SPIKE_OUT} ;
    enum CellRsdnf_Params {NB_SPIKE,PROBA};
    Router();
    virtual void computeState() override;


};

#endif // ROUTER_H
