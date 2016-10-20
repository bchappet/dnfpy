#ifndef SBSFLOATROUTER_H
#define SBSFLOATROUTER_H
#include "bitstreamfloatgenerator.h"
#include "bitstreamfloat.h"

class SBSFloatRouter : public BitStreamFloatGenerator
{
public:

    SBSFloatRouter(int row =0,int col = 0);

    enum SBSFloatRouter_params{SIZE_STREAM};

    virtual void computeState() override{}

    virtual void reset() override;
    
    virtual void setDefaultParams(Module::ParamsPtr params) override;

    virtual BitStreamFloat::BSFPtr getSBS() override;

    void setSynSBS(BitStreamFloat::BSFPtr sbs);


protected:

    BitStreamFloat::BSFPtr sbs;
    BitStreamFloat::BSFPtr synSBS; //will be set by the cell
};

#endif // SBSFLOATROUTER_H
