#ifndef SBSFASTROUTER_H
#define SBSFASTROUTER_H
#include "bitstreamgenerator.h"
#include "bitstreamuint.h"

class SBSFastRouter : public BitStreamGenerator
{
public:

    SBSFastRouter();

    virtual void computeState() override{}

    virtual void reset() override;

    virtual BitStreamUint::BSBPtr getSBS() override;

    void setSynSBS(BitStreamUint::BSBPtr sbs);


protected:

    BitStreamUint::BSBPtr sbs;
    BitStreamUint::BSBPtr synSBS; //will be set by the cell
};

#endif // SBSFASTROUTER_H
