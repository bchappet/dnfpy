#ifndef ROUTER_SEQUENCE_MIXTE_H
#define ROUTER_SEQUENCE_MIXTE_H
#include "routerSequence.h"

/*
 * Router sequence manage its own random numbers
 * it is initialized with a high quality random bit corresponding to the right probability
 * at each iteration the random bit is propagated to neighbours
 *
 * The mixte router generate random numbers on the first neuron coord 0,0
 */
class RouterSequenceMixte : public RouterSequence
{
public:

    RouterSequenceMixte(int row , int col);
    virtual void computeState() override;
protected:

};

/**
 * prng will be generated for each module at the origin of the cycle
 * row = 0 for E and W
 * col = 0 for N and S
 */
class RouterSequenceShortMixte : public RouterSequenceMixte
{
public:
    RouterSequenceShortMixte(int row, int col, int dir):RouterSequenceMixte(row,col),dir(dir){};
    //TODO the design is bad, we should split this method to aviod copy/paste
    virtual void computeState() override;
protected:
    int dir;
};

#endif // ROUTER_SEQUENCE_MIXTE_H
