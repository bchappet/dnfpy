#ifndef BITSTREAMCHAR_H
#define BITSTREAMCHAR_H
#include "bitstream.h"
#include <vector>
/**
  Implementation with vector of bool
 * @brief The BitStreamChar class
 */
class BitStreamChar : public BitStream
{
public:
    BitStreamChar(unsigned int size);
    BitStreamChar(float proba,unsigned int size);

    float mean() override;
    unsigned int count_ones() override;

    friend BitStreamChar operator&(const BitStreamChar &right, const BitStreamChar &left);
    friend BitStreamChar operator|(const BitStreamChar &right, const BitStreamChar &left);


protected:
    std::vector<bool> data;
};

#endif // BITSTREAMCHAR_H
