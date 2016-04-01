#ifndef CELLSBSFAST_H
#define CELLSBSFAST_H
#include "module.h"
#include "bitstreamuint.h"
#include "bitstreamgenerator.h"
/**
 * @brief The CellSBSFast class this kind of cell is a simulation if the BsRsdnf model
 *
 */
class CellSBSFast: public BitStreamGenerator
{
public:
    CellSBSFast(int row=0,int col=0);
    virtual void setDefaultParams(ParamsPtr params) override;


    /**
     * @brief The CellSBSFast_Parameters enum
     * PROBA_SPIKE : prob value of a spike which correspond to 1. in real
     * SIZE_STREAM : the size of the stochastic bit stream that will be generated
     * PROBA_SYNAPSE : for utility now: linked to the PROBA_SYNAPSE of every router
     * PRECISION_PROBA: precision used to generate probability Cannot be dynamically changed (TODO)
     * NB_NEW_RANDOM_BIT: how many new random bit we generate (TODO)
     */
    enum CellSBSFast_Parameters{PROBA_SPIKE,SIZE_STREAM,PROBA_SYNAPSE,PRECISION_PROBA};

    /**
     * @brief The CellRsdnf_Attributes enum
     * NB_BIT_RECEIVED: nb bit received by a cell
     * ACTIVATED is the cell activated (if yes, it will generate a spike SBS)
     * DEAD if its dead (TODO)
     *
     */
    enum CellSBSFast_Attributes{NB_BIT_RECEIVED,ACTIVATED,DEAD};

    virtual BitStreamUint::BSBPtr getSBS() override;

    virtual void preCompute() override;
    virtual void computeState() override;

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

    /**
     * @brief sbs spike sbs
     */
    BitStreamUint::BSBPtr sbs;


};

#endif // CELLSBSFAST_H
