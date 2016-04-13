#ifndef BSROUTER_H
#define BSROUTER_H
#include "module.h"
class BSRouter : public Module
{
public:
    BSRouter();
    virtual void computeState() override;

    enum BSRouter_Parameter{PROBA_SYNAPSE,PRECISION_PROBA};
    virtual void setDefaultParams(Module::ParamsPtr params) override;

    /**
     * @brief The BSRouter_Registers enum
     * BS_OUT : stochastic bit stream outputed
     */
    enum BSRouter_Registers{BS_OUT};

    void setLastRandomNumber(int* intp);

protected:
    int* lastRandomNumber;
};

#endif // BSROUTER_H
