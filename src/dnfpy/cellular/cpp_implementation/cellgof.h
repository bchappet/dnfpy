#ifndef CELLGOF_H
#define CELLGOF_H
#include "module.h"
/**
 * @brief The CellGof class is the game of life implementation
 */
class CellGof : public Module
{
public:
    enum CellGofRegister { STATE} ;

    CellGof(int row=0,int col=0,bool state=false);
    virtual void computeState() override;
};

#endif // CELLGOF_H
