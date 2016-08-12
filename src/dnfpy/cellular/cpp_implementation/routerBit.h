#ifndef ROUTER_BIT_H
#define ROUTER_BIT_H
#include "router.h"

/*
 * RouterBit does not generate its random bit "randomBit" but it is set duting precomputation by the parent cell
 */
class RouterBit : public Router
{
public:

    RouterBit(int row = 0, int col = 0);
    virtual void computeState() override;
    virtual void setDefaultParams(Module::ParamsPtr params) override;
    void setRandomBit(bool bit);
protected:
    bool randomBit;
};

#endif // ROUTER_BIT_H
