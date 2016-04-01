#ifndef CellBsRsdnf_H
#define CellBsRsdnf_H
#include "module.h"
#include <string>

/**
 * @brief The CellBsRsdnf class Cery dirty for now... we assume that precisionProbaSpike == precisionProbaSynapse (in nb bit) 30 for best
 * precision (and fast)
 */
class CellBsRsdnf : public Module
{
public:



    CellBsRsdnf(int row=0,int col=0,std::string typeRouter="orRouter");
    virtual void setDefaultParams(ParamsPtr params) override;
    ~CellBsRsdnf();


    /**
     * @brief The CellBsRsdnf_Parameters enum
     * PROBA_SPIKE : prob value of a spike which correspond to 1. in real
     * SIZE_STREAM : the size of the stochastic bit stream that will be generated
     * PROBA_SYNAPSE : for utility now: linked to the PROBA_SYNAPSE of every router
     * PRECISION_PROBA: precision used to generate probability Cannot be dynamically changed
     * NB_NEW_RANDOM_BIT: how many new random bit we generate
     */
    enum CellBsRsdnf_Parameters{PROBA_SPIKE,SIZE_STREAM,PROBA_SYNAPSE,PRECISION_PROBA,NB_NEW_RANDOM_BIT};

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

    /**
     * @brief lastRandomNumber save the last random number as we may want to use it
     */
    int* lastRandomNumber;




    unsigned long int precisionProbaMask;
};

#endif // CellBsRsdnf_H
