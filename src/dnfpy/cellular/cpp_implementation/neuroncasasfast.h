#ifndef NEURONE_CASAS_FAST_H
#define NEURONE_CASAS_FAST_H
#include "module.h"
#include "bitstreamuint.h"
#include "bitstreamgenerator.h"
/**
 * @brief approximation of the CASAS-DNF
 * The potential is a bit stream updated here 
 * It has 2 layers : excitation and inhibititon
 * The bit stream are used in bipolar representation for the potential we use XNOR for multiplication
 */
class NeuronCasasFast: public BitStreamGenerator
{
public:
    NeuronCasasFast(int row=0,int col=0);
    virtual void setDefaultParams(ParamsPtr params) override;


    /**
     * SIZE_POTENTIAL_STREAM : the potential sbs size default 1000
     * THRESHOLD : number of high bit to activate the neuron default 20
     * PROBA_EXC :
     * PROBA_INH
     * PRECISION_PROBA
     * TAU
     */
    enum NeuronCasaFast_Parameters{SIZE_POTENTIAL_STREAM,THRESHOLD,PROBA_EXC,PROBA_INH,PRECISION_PROBA,TAU};

    /**
     * POTENTIAL : mean of the potential SBS : get only float
     * NB_ACT : number of time that THRESHOLD was crossed : get only int
     * STIM : probability of stimulu : get and set float
     * NB_BIT_EXC : nb bit received by a cell : get only int
     * NB_BIT_INH : nb bit received by a cell : get only int 
     * NB_BIT_STIM : nb bit received by a cell : get only int
     *
     */
    enum CellSBSFast_Attributes{POTENTIAL,NB_ACT,STIM,NB_BIT_EXC,NB_BIT_INH,NB_BIT_STIM};

    virtual BitStreamUint::BSBPtr getSBS() override;
    BitStreamUint::BSBPtr getPotSBS();

    virtual void preCompute() override;
    virtual void computeState() override;

    virtual void getAttribute(int index,void* value) override;

    virtual void setAttribute(int index, void* value) override;

    virtual void reset() override;

protected:
    int nbBitExc,nbBitInh,nbBitStim,nbBitAct;
    float stim;
    /**
     * @brief sbs activation sbs
     */
    BitStreamUint::BSBPtr sbs;
    BitStreamUint::BSBPtr potentialSbs;



};


#endif // CELLSBSFAST_H
