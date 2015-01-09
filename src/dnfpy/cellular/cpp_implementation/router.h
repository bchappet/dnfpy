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
    void setActivated(bool isActivated);
protected:
    bool activated;//controled by cell


};

#endif // ROUTER_H
