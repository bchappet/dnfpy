#ifndef ROUTER_H
#define ROUTER_H
#include "module.h"


class Router : public Module
{
public:
    enum RouterRegister { BUFFER,SPIKE_OUT} ;
    enum RouterParams {PROBA,PRECISION_PROBA};

    Router(int row=0,int col=0);
    virtual void computeState() override;
    virtual void setDefaultParams(Module::ParamsPtr params) override;
protected:
    /**
     * @brief generate a stochastic bit following a bernouilli trial
     * @params proba : float probability of high bit
     * @precision_proba: int precision mask for the probability
     */
    virtual bool bernouilliTrial(float proba,int precision_proba);
};

#endif // ROUTER_H
