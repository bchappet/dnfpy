#ifndef CELLRSDNF_H
#define CELLRSDNF_H
#include "module.h"
#include <string>

class CellRsdnf : public Module
{
public:
    CellRsdnf(int row=0, int col=0,std::string typeRouter="prng");
    virtual void computeState() override;
    virtual void setDefaultParams(ParamsPtr params) override;

    virtual void initRouters(std::string typeRouter);

    enum CellRsdnf_Params {NB_SPIKE};
    enum CellRsdnf_Register {ACTIVATED,NB_BIT_RECEIVED};


protected:
};

#endif // CELLRSDNF_H
