#ifndef ROUTER_SEQUENCE_H
#define ROUTER_SEQUENCE_H
#include "router.h"

/*
 * Router sequence manage its own random numbers
 * it is initialized with a high quality random bit corresponding to the right probability
 * at each iteration the random bit is propagated to neighbours
 *
 * The neighborhood will be augmented of 1 neighbour which will be the random number predecessor.
 */
class RouterSequence : public Router
{
public:
    enum RouterSequenceRegister { BUFFER,SPIKE_OUT,RANDOM_OUT} ;

    RouterSequence(int row =0, int col =0);
    virtual void computeState() override;

protected:
 //   virtual bool bernouilliTrial(float proba,int precision_proba) override;


};

#endif // ROUTER_SEQUENCE_H
