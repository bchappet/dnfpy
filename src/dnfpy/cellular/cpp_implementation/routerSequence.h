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

    RouterSequence();
    virtual void computeState() override;

    //void setActivated(bool isActivated);
protected:
    //bool activated;//controled by cell


};

#endif // ROUTER_SEQUENCE_H
