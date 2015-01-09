#include "bitstreamutils.h"
#include <stdlib.h>     /* srand, rand */

#define PRECISION_RAND 1000000


bool generateStochasticBit(float proba){
    int randInt = rand() % PRECISION_RAND;
    return randInt <= (proba * PRECISION_RAND);

}
