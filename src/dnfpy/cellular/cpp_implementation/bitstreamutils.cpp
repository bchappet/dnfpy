#include "bitstreamutils.h"
#include <stdlib.h>     /* srand, rand */
#include <ctime>
#include <iostream>

#define PRECISION_RAND 1000000

static int seedCount = 0;

bool generateStochasticBit(float proba){
    int randInt = rand() % PRECISION_RAND;
    return randInt <= (proba * PRECISION_RAND);

}

void initSeed(){
    std::cout << "seed count " << seedCount << std::endl;
    srand (seedCount);
    seedCount ++;
}
