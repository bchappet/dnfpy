#ifndef CELLSBSFLOAT_H
#define CELLSBSFLOAT_H
#include "module.h"
#include "bitstreamfloat.h"
#include "bitstreamfloatgenerator.h"
/**
 * @brief The CellSBSFloat class 
 *  Describe a cell simulating assymptotic behavior of SBSFast cell 
 *
 */
class CellSBSFloat: public BitStreamFloatGenerator
{
public:
    CellSBSFloat(int row=0,int col=0);
    virtual void setDefaultParams(ParamsPtr params) override;


    /**
     * @brief The CellSBSFloat_Parameters enum
     * PROBA_SPIKE : prob value of a spike which correspond to 1. in real
     * SIZE_STREAM : the size of the stochastic bit stream that will be generated
     * PROBA_SYNAPSE : for utility now: linked to the PROBA_SYNAPSE of every router
     * PRECISION_PROBA: precision used to generate probability Cannot be dynamically changed (TODO)
     */
    enum CellSBSFloat_Parameters{PROBA_SPIKE,SIZE_STREAM,PROBA_SYNAPSE,PRECISION_PROBA};

    /**
     * @brief The CellRsdnf_Attributes enum
     * VALUE : (float) value of the cell ie sum of incoming sbs
     * ACTIVATED is the cell activated (if yes, it will generate a spike SBS)
     * DEAD if its dead (TODO)
     *
     */
    enum CellSBSFloat_Attributes{VALUE,ACTIVATED,DEAD};

    virtual BitStreamFloat::BSFPtr getSBS() override;

    virtual void preCompute() override;
    virtual void computeState() override;

    virtual void getAttribute(int index,void* value) override;

    virtual void setAttribute(int index, void* value) override;

    virtual void reset() override;

protected:
    /**
     * @brief sum of incoming sbs 
     */
    float value;
    /**
     * @brief activated if true the cell will emmit NB_SPIKE spikes and will set this.activated at false
     */
    bool activated;
    /**
     * @brief dead if true, the cell will do nothing on spike reception
     */
    bool dead;

    /**
     * @brief spike sbs
     */
    BitStreamFloat::BSFPtr sbs;


};

#endif // CELLSBSFLOAT_H
