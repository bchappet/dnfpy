#ifndef BITSTREAMGENERATOR_H
#define BITSTREAMGENERATOR_H
#include "module.h"
#include "bitstreamuint.h"

class BitStreamGenerator : public Module
{
public:
    virtual BitStreamUint::BSBPtr getSBS() = 0;
};

#endif // BITSTREAMGENERATOR_H
