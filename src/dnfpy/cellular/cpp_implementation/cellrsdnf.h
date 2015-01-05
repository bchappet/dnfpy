#ifndef CELLRSDNF_H
#define CELLRSDNF_H
#include "module.h"
class CellRsdnf : public Module
{
public:
    enum CellRsdnf_Register { POTENTIAL,ACTIVATED_OUT} ;

    CellRsdnf();
    virtual void computeState() override;
};

#endif // CELLRSDNF_H
