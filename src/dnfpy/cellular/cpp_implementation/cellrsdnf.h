#ifndef CELLRSDNF_H
#define CELLRSDNF_H
#include "module.h"
#include <string>

class CellRsdnf : public Module
{
public:
    CellRsdnf(std::string typeRouter="prng");
    virtual void computeState() override;
    virtual void setDefaultParams(ParamsPtr params) override;

    virtual void initRouters(std::string typeRouter);

    enum CellRsdnf_Attributes{NB_BIT_RECEIVED,ACTIVATED,DEAD};
    enum CellRsdnf_Params {NB_SPIKE,PROBA,PRECISION_PROBA};


    virtual void getAttribute(int index,void* value) override;


    virtual void setAttribute(int index, void* value) override;

    virtual void reset() override;

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
};

#endif // CELLRSDNF_H
