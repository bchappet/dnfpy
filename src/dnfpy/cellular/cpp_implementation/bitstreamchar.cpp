#include "bitstreamchar.h"
#include "bitstreamutils.h"
BitStreamChar::BitStreamChar(unsigned int size):BitStream(size)
{
    this->data = std::vector<bool>(size);
}

BitStreamChar::BitStreamChar(float proba, unsigned int size):BitStreamChar(size)
{
    for(unsigned int i = 0 ; i < size; ++i){
        this->data[i] = generateStochasticBit(proba,PRECISION_MAX);
    }
}



float BitStreamChar::mean(){

    return this->count_ones()/float(this->size);
}

unsigned int BitStreamChar::count_ones(){
    unsigned int sum = 0;
    for(unsigned int i = 0 ; i < this->size; ++i){
         sum += this->data[i];
    }
    return sum;
}



BitStreamChar operator&(const BitStreamChar &right, const BitStreamChar &left){
    BitStreamChar res = BitStreamChar(right.size);
    for(unsigned int i = 0 ; i < right.size; ++i){
        res.data[i] = right.data[i] & left.data[i];
    }
    return res;
}

BitStreamChar operator|(const BitStreamChar &right, const BitStreamChar &left){
    BitStreamChar res = BitStreamChar(right.size);
    for(unsigned int i = 0 ; i < right.size; ++i){
        res.data[i] = right.data[i] | left.data[i];
    }
    return res;
}
