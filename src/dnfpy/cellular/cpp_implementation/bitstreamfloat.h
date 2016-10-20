#ifndef BITSTREAMFLOAT_H
#define BITSTREAMFLOAT_H
#include "bitstream.h"
#include <inttypes.h>
#include <vector>
#include <iostream>
#include "bitstreamutils.h"
#include <boost/smart_ptr.hpp>

/**
 * BitStreamFloat 
 * Assymptotic representation of a bitstream
 * Its value is encoded by a float directly
 *
 */
class BitStreamFloat : public BitStream
{
public:
    typedef boost::shared_ptr<BitStreamFloat> BSFPtr;
    /** Construct a 0 bitstream with size bits**/
    BitStreamFloat(unsigned int size);
    /** Copy constructor**/
    BitStreamFloat(const BitStreamFloat &sbs);
    BitStreamFloat(float proba,unsigned int size,u_int32_t  probaMask = PRECISION_MAX);





    virtual unsigned int count_ones() override;
    virtual float mean() override;




    /*AND return a*b*/
    BitStreamFloat& operator &= (const BitStreamFloat &left) ;
    friend BitStreamFloat operator&(const BitStreamFloat &right, const BitStreamFloat &left);

    /*OR return a+b - a*b*/
    BitStreamFloat& operator |= (const BitStreamFloat &left) ;
    friend BitStreamFloat operator|(const BitStreamFloat &right, const BitStreamFloat &left);


    /*MUX return (a+b)/2*/
    friend BitStreamFloat operator+(const BitStreamFloat &right, const BitStreamFloat &left);


    friend BitStreamFloat operator~(const BitStreamFloat &bs);
    friend std::ostream& operator << (std::ostream &os, const BitStreamFloat& bs);

protected:

    unsigned int size; //should used in count_one for backward compatibility
    float value; //actual value of the BS
};

#endif // BITSTREAMFLOAT_H
