#ifndef BITSTREAMUTILS_H
#define BITSTREAMUTILS_H
#include<vector>
#include<stdint.h>

extern "C" {


    const uint32_t PRECISION_MAX = 0x7fffffff;//for some reason rand return 31 bits

    void initSeed(long int seed);
    /**
     * @brief generateStochasticBit
     * @param proba probability
     * @param precisionMask precision of the random bit : rand() & precision
     * @return
     */
    bool generateStochasticBit(float proba,uint32_t precisionMask=PRECISION_MAX);

    uint32_t genRandInt(uint32_t randomBitMask=PRECISION_MAX);
    bool getRandBitFromRandInt(uint32_t randInt, float proba,uint32_t precisionMask=PRECISION_MAX);

    std::vector<uint32_t> generateRotatedBitChunck32(unsigned int nb,std::vector<float> probaVec, unsigned int shift,unsigned int nbCommonBit,
                                                      uint32_t randomBitMask=PRECISION_MAX,uint32_t precisionMask=PRECISION_MAX);
    uint32_t generateBitChunck32(float proba,uint32_t precisionMask,unsigned int nbBit = 31);



    /**
     * @brief rotation left of the randInt number
     * @param shift : nb bit for rotation
     * @param nbBit : nb bit considered in the randomInt number
     * @param mask : mask of the randomInt number should be 2^nbBit -1
     */
    uint32_t rotl32(uint32_t randInt, unsigned int shift, unsigned int nbBit,uint32_t mask);


    /**
     * @brief generateStochasticBit
     * @param proba probability
     * @param precision precision of the random bit : rand() % precision
     * @param lastRandomNumber : the last random number used by the ressource
     * @param nbBitToGenerate : nb bit to share between last random number and new one
     * @return
     */
    bool generateStochasticBitWithReutilisation(float proba,int precision,int* lastRandomNumber,int nbNewBitToGenerate);

}

 std::vector<uint64_t> newSBS(float proba,unsigned int size);

 void printSBS(std::vector<uint64_t>);

 unsigned int count_ones(std::vector<uint64_t> sbs);

 float meanSBS(std::vector<uint64_t> sbs);

 std::vector<uint64_t> operator|(std::vector<uint64_t> a,std::vector<uint64_t> b);

 std::vector<uint64_t> operator&(std::vector<uint64_t> a,std::vector<uint64_t> b);


#endif
