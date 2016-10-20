#ifndef BITSTREAMFLOATGENERATOR_H
#define BITSTREAMFLOATGENERATOR_H
#include "module.h"
#include "bitstreamfloat.h"

class BitStreamFloatGenerator : public Module
{
public:
    BitStreamFloatGenerator(int row=0,int col=0) : Module(row,col){};
    virtual BitStreamFloat::BSFPtr getSBS() = 0;
};

#endif // BITSTREAMFLOATGENERATOR_H
