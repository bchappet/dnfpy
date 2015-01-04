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
    CellGof(bool state=false);
    virtual void computeState() override;
};

#endif // CELLGOF_H
