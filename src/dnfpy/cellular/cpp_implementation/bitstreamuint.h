#ifndef BITSTREAMUINT_H
#define BITSTREAMUINT_H
#include "bitstream.h"
#include <inttypes.h>
#include <vector>
#include <iostream>
#include "bitstreamutils.h"
#include <boost/smart_ptr.hpp>

class BitStreamUint : public BitStream
{
public:
    typedef boost::shared_ptr<BitStreamUint> BSBPtr;
    BitStreamUint(unsigned int size);
    BitStreamUint(float proba,unsigned int size,u_int32_t  probaMask = PRECISION_MAX);




    virtual unsigned int count_ones() override;
    virtual float mean() override;

    void copy(const BitStreamUint &sbs);


    BitStreamUint& operator &= (const BitStreamUint &left) ;
    BitStreamUint& operator |= (const BitStreamUint &left) ;


    friend std::vector<BSBPtr> genRotatedSBS(unsigned int nbSBS,std::vector<float> probaVec,int size,unsigned int shift=1,unsigned int nbCommonBit=31, u_int32_t precisionMask=PRECISION_MAX);
    friend BitStreamUint operator&(const BitStreamUint &right, const BitStreamUint &left);
    friend BitStreamUint operator|(const BitStreamUint &right, const BitStreamUint &left);
    friend std::ostream& operator << (std::ostream &os, const BitStreamUint& bs);

protected:
    bool simpleValue;//true if we want to store p=1 or p=0
    bool value; //if simple value, the value will be here
    unsigned int vecSize; //size of the vec
    std::vector<uint32_t> data;
    uint32_t mask; //mask for the last uint32_t chunck
};

std::vector<BitStreamUint::BSBPtr> genRotatedSBS(unsigned int nbSBS,std::vector<float> probaVec,int size,unsigned int shift,unsigned int nbCommonBit, u_int32_t precisionMask);
#endif // BITSTREAMUINT_H
