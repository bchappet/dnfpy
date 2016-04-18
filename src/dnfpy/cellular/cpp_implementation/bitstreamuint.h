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
    /** Construct a 0 bitstream with size bits**/
    BitStreamUint(unsigned int size,bool initMem=false);
    /** Copy constructor**/
    BitStreamUint(const BitStreamUint &sbs);
    BitStreamUint(float proba,unsigned int size,u_int32_t  probaMask = PRECISION_MAX);

    void setIndex(int index);
    int getIndex();




    virtual unsigned int count_ones() override;
    virtual float mean() override;

    /**
    * @brief BitStreamUint::copy copy another bitstream, uint by uint
    * @param sbs
    */
    void copy(const BitStreamUint &sbs);

    /**
     * detect threshold number of spike
     */
    BitStreamUint applyCounter(const unsigned int threshold, const unsigned int size);


    BitStreamUint& operator &= (const BitStreamUint &left) ;
    BitStreamUint& operator |= (const BitStreamUint &left) ;
    //wrapped rotation of the bit stream
    BitStreamUint operator << (const unsigned int shift) const;


    friend std::vector<BSBPtr> genRotatedSBS(unsigned int nbSBS,std::vector<float> probaVec,int size,unsigned int shift=1,unsigned int nbCommonBit=31, u_int32_t precisionMask=PRECISION_MAX);
    friend BitStreamUint operator&(const BitStreamUint &right, const BitStreamUint &left);
    friend BitStreamUint operator|(const BitStreamUint &right, const BitStreamUint &left);
    /*MUX*/
    friend BitStreamUint operator+(const BitStreamUint &right, const BitStreamUint &left);
    /*XOR*/
    friend BitStreamUint operator^(const BitStreamUint &right, const BitStreamUint &left);
    friend BitStreamUint operator~(const BitStreamUint &bs);
    friend std::ostream& operator << (std::ostream &os, const BitStreamUint& bs);

protected:

    /**
     * Return a rotated version of a chunck
     */
    u_int32_t rotatedChunck(const BitStreamUint &sbs,unsigned int chunckIndex, unsigned int shift) const;
    u_int32_t getData(unsigned int chunckIndex) const;

    bool simpleValue;//true if we want to store p=1 or p=0
    bool value; //if simple value, the value will be here
    unsigned int vecSize; //size of the vec
    std::vector<uint32_t> data;
    uint32_t mask; //mask for the last uint32_t chunck
    unsigned int index; //operation will start from this index TODO
};

std::vector<BitStreamUint::BSBPtr> genRotatedSBS(unsigned int nbSBS,std::vector<float> probaVec,int size,unsigned int shift,unsigned int nbCommonBit, u_int32_t precisionMask);
#endif // BITSTREAMUINT_H
