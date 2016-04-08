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


    enum CellRsdnf2_Reg{NB_BIT_INH_RECEIVED=3};
    enum CellRsdnf2_Params {PROBA=1,PRECISION_PROBA=2,PROBA_INH=3,PRECISION_RANDOM=4,NB_BIT_RANDOM=5,SHIFT=6};



};

#endif // CELLRSDNF2_H
