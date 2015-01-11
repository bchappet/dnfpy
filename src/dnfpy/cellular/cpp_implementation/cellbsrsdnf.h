#ifndef CellBsRsdnf_H
#define CellBsRsdnf_H
#include "module.h"
#include <string>
class CellBsRsdnf : public Module
{
public:

    CellBsRsdnf(std::string typeRouter="routerAdditionOr");



    /**
     * @brief The CellBsRsdnf_Parameters enum
     * PROBA_SPIKE : prob value of a spike which correspond to 1. in real
     * SIZE_STREAM : the size of the stochastic bit stream that will be generated
     * PROBA_SYNAPSE : for utility now: linked to the PROBA_SYNAPSE of every router
     */
    enum CellBsRsdnf_Parameters{PROBA_SPIKE,SIZE_STREAM,PROBA_SYNAPSE};

    /**
     * @brief The CellBsRsdnf_Registers enum
     * SPIKE_BS: the stochastic bit stream of the spike, sent on activation
     */
    enum CellBsRsdnf_Registers{SPIKE_BS};


    enum CellRsdnf_Attributes{NB_BIT_RECEIVED,ACTIVATED,DEAD};

    virtual void computeState() override;


    virtual void getAttribute(int index,void* value) override;


    virtual void setAttribute(int index, void* value) override;



protected:
    /**
     * @brief nbBitReceived nb bit received since last reset
     */
    int nbBitReceived;
    /**
     * @brief activated if true the cell will emmit NB_SPIKE spikes and will set this.activated at false
     */
    bool activated;
    /**
     * @brief dead if true, the cell will do nothing on spike reception
     */
    bool dead;

    /**
     * @brief nbBitToGenerate, if activated, we have SIZE_STREAM bit to generate
     * not accessible from outside
     */
    int nbBitToGenerate;
};

#endif // CellBsRsdnf_H
