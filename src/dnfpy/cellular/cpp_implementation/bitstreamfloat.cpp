#include "bitstreamfloat.h"

BitStreamFloat::BitStreamFloat(unsigned int size):BitStream(size){
    this->value = 0;
}

BitStreamFloat::BitStreamFloat(const BitStreamFloat &sbs):BitStream(sbs.size){
    this->value = sbs.value;
}

BitStreamFloat::BitStreamFloat(float proba,unsigned int size, u_int32_t  probaMask):BitStream(size){
    this->size = size;
    this->value = floor(proba*probaMask)/(float)probaMask;
}

unsigned int BitStreamFloat::count_ones(){
    return round(this->size * this->value);
}

float BitStreamFloat::mean() {
    return this->value;
}

BitStreamFloat& BitStreamFloat::operator &= (const BitStreamFloat &left) {
    this->value = this->value * left.value;
    return *this;
}

BitStreamFloat& BitStreamFloat::operator |= (const BitStreamFloat &left){
    this->value = this->value + left.value - (this->value * left.value);
    return *this;
}

BitStreamFloat operator&(const BitStreamFloat &right, const BitStreamFloat &left){
    return BitStreamFloat(right.value *left.value,right.size);
}

BitStreamFloat operator|(const BitStreamFloat &right, const BitStreamFloat &left){
    return BitStreamFloat(right.value +left.value - (right.value*left.value) ,right.size);
}

BitStreamFloat operator+(const BitStreamFloat &right, const BitStreamFloat &left){
    return BitStreamFloat((right.value +left.value)/2.0,right.size);
}

BitStreamFloat operator~(const BitStreamFloat &bs){
    return BitStreamFloat(1-bs.value,bs.size);
}

std::ostream& operator << (std::ostream &os, const BitStreamFloat& bs){
    os << bs.value;
    return os;
}
