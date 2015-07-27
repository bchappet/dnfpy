#ifndef BITSTREAM_H
#define BITSTREAM_H

class BitStream
{
public:
    BitStream(unsigned int size);
    virtual float mean() = 0;
    virtual unsigned int count_ones() = 0;


    unsigned int size;




};

#endif // BITSTREAM_H
