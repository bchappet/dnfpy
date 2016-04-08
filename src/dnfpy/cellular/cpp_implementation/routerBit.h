#ifndef ROUTER_BIT_H
#define ROUTER_BIT_H
#include "router.h"

/*
 * RouterBit does not generate its random numbers RANDOM_OUT but there are set duting precomputation by the parent cell
 */
class RouterBit : public Router
{
public:
    enum RouterBitRegistre {RANDOM_BIT=2};

    RouterBit(int row = 0, int col = 0);
    virtual void computeState() override;
    virtual void setDefaultParams(Module::ParamsPtr params) override;



};

#endif // ROUTER_BIT_H
