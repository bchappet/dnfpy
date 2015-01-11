#ifndef CARRYBSROUTER_H
#define CARRYBSROUTER_H
#include "module.h"
class CarryBsRouter : public Module
{
public:
    CarryBsRouter();
    virtual void computeState() override;
    /**
     * @brief The BSRouter_Registers enum
     * BS_OUT : stochastic bit stream outputed
     * CARRY : save bits that where not send
     */
    enum CarryBSRouter_Registers{BS_OUT,CARRY};

    /**
     * @brief The BSRouter_Parameters enum
     * PROBA_SYNAPSE : to generate the synaptic weight flux.
     */
    enum CarryBSRouter_Parameters{PROBA_SYNAPSE};
};

#endif // CARRYBSROUTER_H
