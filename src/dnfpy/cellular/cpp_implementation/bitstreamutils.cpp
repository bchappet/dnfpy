#include "bitstreamutils.h"
#include <stdlib.h>     /* srand, rand */
#include <ctime>
#include <iostream>
#include <math.h>
#include <algorithm>    // std::max
#include <bitset>




bool generateStochasticBit(float proba,u_int32_t precisionMask){
    u_int32_t randInt = genRandInt(precisionMask);
    //std::cout << "res : " << std::bitset<32>(randInt) << " <= " << proba << " * " << std::bitset<32>(precisionMask) << std::endl;
    //std::cout << "proba * prec : " << std::bitset<32>(proba*precisionMask) << std::endl;
    return getRandBitFromRandInt(randInt,proba,precisionMask);
    //return randInt <= (0x0000ffff);

}

u_int32_t genRandInt(u_int32_t randomBitMask){
    return rand() & randomBitMask;
}

bool getRandBitFromRandInt(u_int32_t randInt, float proba,u_int32_t precisionMask){
    return randInt <= proba * precisionMask;
}

/**
* @brief rotation left of the randInt number
* @param shift : nb bit for rotation
* @param nbBit : nb bit considered in the randomInt number
* @param mask : mask of the randomInt number should be 2^nbBit -1
*/
uint32_t rotl32(uint32_t randInt, unsigned int shift, unsigned int nbBit,uint32_t mask){
    return ((randInt << shift)&mask) | (randInt >> (nbBit - shift));
}

u_int32_t generateBitChunck32(float proba,u_int32_t precisionMask,unsigned int nbBit){
    u_int32_t res = 0;
    for(unsigned int i = 0 ; i < nbBit; ++i){
        bool randBit =  generateStochasticBit(proba,precisionMask);
        res = res << 1;
        res |= randBit;
    }
    return res;
}

std::vector<u_int32_t> generateRotatedBitChunck32(unsigned int nb,std::vector<float> probaVec, unsigned int shift,unsigned int nbCommonBit,
                                                  u_int32_t randomBitMask,u_int32_t precisionMask){
    std::vector<u_int32_t> res = std::vector<u_int32_t>(nb);
    for(unsigned int i = 0 ; i < 32 ;++i){
        //std::cout << "New Rand Int" << std::endl;
        u_int32_t randInt = genRandInt(randomBitMask);

        for(unsigned int chunckId = 0 ; chunckId < nb; ++chunckId){
            //std::cout << "randInt : " << std::bitset<32>(randInt) << std::endl;
            bool randBit = getRandBitFromRandInt(randInt&precisionMask, probaVec[chunckId], precisionMask);
            res[chunckId] = res[chunckId] << 1;
            res[chunckId] |= randBit;
            //rotate the randInt
            randInt = rotl32(randInt,shift,nbCommonBit,randomBitMask);
        }
    }
    return res;
}

void initSeed(int long seed){
    srand (seed);
}

u_int64_t generateBitChunck(float proba,u_int64_t precisionMask){
    unsigned long int res = 0;
    for(unsigned int i = 0 ; i < 64; i++){
        unsigned short randInt =  generateStochasticBit(proba,precisionMask);
        res = res << 1;
        res |= randInt;
    }
    return res;
}

std::vector<u_int64_t> newSBS(float proba,unsigned int size){
    u_int64_t precisionMask = PRECISION_MAX;
    unsigned int vecSize = ceil(size/64.);//each cell contains 64 bits
    std::vector<u_int64_t> vec = std::vector<u_int64_t>(vecSize);
    for(unsigned int i = 0 ; i < vecSize ; ++i){
           vec[i] = generateBitChunck(proba,precisionMask);
    }
    return vec;
}

void printSBS(std::vector<u_int64_t> sbs){
    for(unsigned int i = 0 ; i < sbs.size() ; ++i){
        std::cout << i << ":"<< sbs[i] << std::endl;
    }
}

unsigned int count_ones(std::vector<u_int64_t> sbs){
    unsigned int sum = 0;
    u_int32_t mask32b = 0xFFFFFFFF;
    for(unsigned int i = 0 ; i < sbs.size() ; ++i){
        u_int32_t a = sbs[i] & mask32b;
        u_int32_t b = (sbs[i] >> 32) & mask32b;
        unsigned int count =  __builtin_popcount(a) + __builtin_popcount(b);
        //std::cout << "i : " << i << " count " << count << std::endl;
        sum += count;
    }
    return sum;
}

float meanSBS(std::vector<u_int64_t> sbs){
    float tot = sbs.size()*64;
    return count_ones(sbs)/tot;
}


std::vector<u_int64_t> operator|(std::vector<u_int64_t> a,std::vector<u_int64_t> b){
    unsigned int size = a.size();
    std::vector<u_int64_t> res = std::vector<u_int64_t>(size);
    for(unsigned int i = 0 ; i < size ;++i){
        res[i] = a[i] | b[i];
    }
    return res;
}

std::vector<u_int64_t> operator&(std::vector<u_int64_t> a,std::vector<u_int64_t> b){
    unsigned int size = a.size();
    std::vector<u_int64_t> res = std::vector<u_int64_t>(size);
    for(unsigned int i = 0 ; i < size ;++i){
        res[i] = a[i] & b[i];
    }
    return res;
}




