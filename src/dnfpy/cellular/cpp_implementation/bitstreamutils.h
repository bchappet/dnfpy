#ifndef BITSTREAMUTILS_H
#define BITSTREAMUTILS_H
#include<vector>
#include<stdint.h>

extern "C" {

    const uint32_t ONE_BIT[32] = {0x1,0x2,0x4,0x8,
                        0x10,0x20,0x40,0x80,
                        0x100,0x200,0x400,0x800,
                        0x1000,0x2000,0x4000,0x8000,
                        0x10000,0x20000,0x40000,0x80000,
                        0x100000,0x200000,0x400000,0x800000,
                        0x1000000,0x2000000,0x4000000,0x8000000,
                        0x10000000,0x20000000,0x40000000,0x80000000
    };

    const uint32_t LOW_MASK[32] = {0x1,0x3,0x7,0xf,
                                    0x1f,0x3f,0x7f,0xff,
                                    0x1ff,0x3ff,0x7ff,0xfff,
                                    0x1fff,0x3fff,0x7fff,0xffff,
                                    0x1ffff,0x3ffff,0x7ffff,0xfffff,
                                    0x1fffff,0x3fffff,0x7fffff,0xffffff,
                                    0x1ffffff,0x3ffffff,0x7ffffff,0xfffffff,
                                    0x1fffffff,0x3fffffff,0x7fffffff,0xffffffff,
    };

    const uint32_t HIGH_MASK[32] = {
        0x80000000,
        0xc0000000,
        0xe0000000,
        0xf0000000,
        0xf8000000,
        0xfc000000,
        0xfe000000,
        0xff000000,
        0xff800000,
        0xffc00000,
        0xffe00000,
        0xfff00000,
        0xfff80000,
        0xfffc0000,
        0xfffe0000,
        0xffff0000,
        0xffff8000,
        0xffffc000,
        0xffffe000,
        0xfffff000,
        0xfffff800,
        0xfffffc00,
        0xfffffe00,
        0xffffff00,
        0xffffff80,
        0xffffffc0,
        0xffffffe0,
        0xfffffff0,
        0xfffffff8,
        0xfffffffc,
        0xfffffffe,
        0xffffffff,
    };




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
    uint32_t generateBitChunck32(float proba,uint32_t precisionMask,unsigned int nbBit = 32);



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
