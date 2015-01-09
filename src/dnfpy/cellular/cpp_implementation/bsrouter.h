#ifndef BSROUTER_H
#define BSROUTER_H
#include "module.h"
class BSRouter : public Module
{
public:
    BSRouter();
    virtual void computeState() override;
    /**
     * @brief The BSRouter_Registers enum
     * BS_OUT : stochastic bit stream outputed
     */
    enum BSRouter_Registers{BS_OUT};

    /**
     * @brief The BSRouter_Parameters enum
     * PROBA_SYNAPSE : to generate the synaptic weight flux.
     */
    enum BSRouter_Parameters{PROBA_SYNAPSE};
};

#endif // BSROUTER_H
