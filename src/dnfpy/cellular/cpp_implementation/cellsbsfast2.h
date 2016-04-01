#ifndef CELLSBSFAST2_H
#define CELLSBSFAST2_H
#include "cellsbsfast.h"

//The same as CellSBSFast, but with two layer: inhibitory and excitatory
class CellSBSFast2 : public CellSBSFast
{
public:
    CellSBSFast2(int row=0,int col=0);

    virtual void setDefaultParams(ParamsPtr params) override;
    virtual void preCompute() override;
    virtual void computeState() override;
    virtual void reset() override;
    virtual void getAttribute(int index,void* value) override;
    virtual void setAttribute(int index, void* value) override;


    enum CellSBSFast2_Parameters{PROBA_SYNAPSE_INH=4,SHIFT=5,NB_SHARED_BIT=6};
    enum CellSBSFast_Attributes{NB_BIT_INH_RECEIVED=3};

protected:
    //2cd layer
    int nbInhBitReceived;
};

#endif // CELLSBSFAST2_H

