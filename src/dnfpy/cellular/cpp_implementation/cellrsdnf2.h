#ifndef CELLRSDNF2_H
#define CELLRSDNF2_H
#include "module.h"
#include <string>
#include "cellrsdnf.h"

/**
 * Like cell rsdnf but with two layers in one in order to share the random number
 */
class CellRsdnf2 : public CellRsdnf
{
public:
    CellRsdnf2(int row,int col);
    virtual void computeState() override;
    virtual void preCompute() override;
    virtual void setDefaultParams(ParamsPtr params) override;


    enum CellRsdnf2_Attributes{NB_BIT_INH_RECEIVED=3};
    enum CellRsdnf2_Params {PROBA_INH=3,PRECISION_RANDOM=4,NB_BIT_RANDOM=5,SHIFT=6};


    virtual void getAttribute(int index,void* value) override;


    virtual void setAttribute(int index, void* value) override;

    virtual void reset() override;

protected:
    /**
     * @brief nbBitInhReceived nb bit received since last reset
     */
    int nbBitInhReceived;
};

#endif // CELLRSDNF2_H
