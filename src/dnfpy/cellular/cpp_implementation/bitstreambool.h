#ifndef BITSTREAMBOOL_H
#define BITSTREAMBOOL_H
#include "bitstream.h"
#include <ostream>
class BitStreamBool : public BitStream
{
public:
    BitStreamBool();
    BitStreamBool(float prob);

    unsigned int count_ones();
    float mean();

    friend BitStreamBool operator&(const BitStreamBool &right, const BitStreamBool &left);
    friend BitStreamBool operator|(const BitStreamBool &right, const BitStreamBool &left);
    friend std::ostream& operator << (std::ostream &os, const BitStreamBool& bs);


protected:
    bool sbs;
};

#endif // BITSTREAMBOOL_H
