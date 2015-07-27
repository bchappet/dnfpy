#include "bitstreambool.h"
#include "bitstreamutils.h"
#include <bitset>
BitStreamBool::BitStreamBool():BitStream(1)
{
    this->sbs = false;
}

BitStreamBool::BitStreamBool(float prob):BitStreamBool(){
    this->sbs = generateStochasticBit(prob,PRECISION_MAX);
}

unsigned int BitStreamBool::count_ones(){
    return this->sbs;
}

float BitStreamBool::mean(){
    return this->sbs;
}

BitStreamBool operator&(const BitStreamBool &right, const BitStreamBool &left){
    BitStreamBool res;
    res.sbs = right.sbs & left.sbs;
    return res;
}

BitStreamBool operator|(const BitStreamBool &right, const BitStreamBool &left){
    BitStreamBool res;
    res.sbs = right.sbs | left.sbs;
    return res;
}

std::ostream& operator<< (std::ostream &os, const BitStreamBool& sbs){
    os << std::bitset<1>(sbs.sbs);
    return os;
 }
