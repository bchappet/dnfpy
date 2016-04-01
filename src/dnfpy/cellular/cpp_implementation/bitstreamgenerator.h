#ifndef BITSTREAMGENERATOR_H
#define BITSTREAMGENERATOR_H
#include "module.h"
#include "bitstreamuint.h"

class BitStreamGenerator : public Module
{
public:
    BitStreamGenerator(int row=0,int col=0) : Module(row,col){};
    virtual BitStreamUint::BSBPtr getSBS() = 0;
};

#endif // BITSTREAMGENERATOR_H
