#include "bitstreamuint.h"
#include "bitstreamutils.h"
#include <math.h>
#include <bitset>

BitStreamUint::BitStreamUint(unsigned int size):BitStream(size)
{

    this->vecSize = ceil(size/32.);
    //The mask will be applied to the last chunck only for decoding
    this->mask = pow(2,size % 32)-1;
    if(this->mask == 0){
        this->mask = 0xffffffff; //2^32-1
    }
    this->simpleValue = true;
    this->value = false;

    // std::cout << " masks " << std::bitset<32>(this->mask) << std::endl;
}


BitStreamUint::BitStreamUint(float proba,unsigned int size,u_int32_t probaMask):BitStreamUint(size){
    if(proba >= 1. || proba <= 0.){
        this->simpleValue = true;
        if(proba >= 1){
            this->value = true;
        }else{
            this->value = false;
        }
    }else{ //proba is not simple
        this->simpleValue = false;
        this->data = std::vector<u_int32_t>(this->vecSize);
        for(unsigned int i = 0 ; i < this->vecSize-1 ; ++i){
            this->data[i] = generateBitChunck32(proba,probaMask,32);
        }
        this->data[this->vecSize-1] = generateBitChunck32(proba,probaMask,this->size%32);
    }
}



unsigned int BitStreamUint::count_ones(){
    unsigned int sum = 0;
    if(this->simpleValue){
        sum = this->value * this->size;
    }else{
        for(unsigned int i = 0 ; i < this->data.size()-1 ; ++i){
            sum += __builtin_popcount(this->data[i]);
        }

        //last chunk: we apply mask
        sum += __builtin_popcount(this->data[this->data.size()-1] & this->mask);
    }

    return sum;
}

float BitStreamUint::mean(){
    unsigned int sum = count_ones();
    return sum/float(this->size);

}

/**
 * @brief BitStreamUint::copy copy another bitstream, uint by uint
 * @param sbs
 */
void BitStreamUint::copy(const BitStreamUint  &sbs){
    this->size = sbs.size;
    this->mask = sbs.mask;
    this->simpleValue = sbs.simpleValue;
    this->value = sbs.value;
    this->data = std::vector<u_int32_t>(sbs.data.size());
    for(unsigned int i = 0 ; i < sbs.data.size(); ++i){
        this->data[i] = sbs.data[i];
    }
}

BitStreamUint& BitStreamUint::operator &= (const BitStreamUint &left){
    if(this->simpleValue){
        if(this->value){
            //if this is true, the result will be left
            this->copy(left);
        }else{
            //if this is false, the result will be false
        }
    }else if(left.simpleValue){
        if(left.value){
            //if left is true, this will be unchanged
        }else{
            //if left is false, this will be false
            this->copy(left);
        }
    }else{
        for(unsigned int i = 0 ; i < this->data.size() ; ++i){
            this->data[i] &= left.data[i];
        }
    }
    return *this;
}


BitStreamUint& BitStreamUint::operator|= (const BitStreamUint &left){
    //std::cout << "size this "<< this->data.size() << std::endl;
    //std::cout << "size left "<< left.data.size() << std::endl;
    if(this->simpleValue){
        if(this->value){
            //if this is true, the result will be true
        }else{
            //if this is false, the result will be left
            this->copy(left);
        }
    }else if(left.simpleValue){
        if(left.value){
            //if left is true, this will be true
            this->copy(left);
        }else{
            //if left is false, this will be unchanged
        }
    }else{
        for(unsigned int i = 0 ; i < this->data.size() ; ++i){
            this->data[i] |= left.data[i];
        }
    }
    return *this;
}





BitStreamUint operator&(const BitStreamUint &right, const BitStreamUint &left){
    BitStreamUint res = BitStreamUint(right.size);
    for(unsigned int i = 0 ; i < right.data.size() ; ++i){
        res.data[i] = right.data[i] & left.data[i];
    }
    return res;
}

BitStreamUint operator|(const BitStreamUint &right, const BitStreamUint &left){
    BitStreamUint res = BitStreamUint(right.size);
    for(unsigned int i = 0 ; i < right.data.size() ; ++i){
        res.data[i] = right.data[i] | left.data[i];
    }
    return res;
}

std::ostream& operator<< (std::ostream &os, const BitStreamUint& sbs){
    if(sbs.simpleValue){
        os << sbs.value;
    }else{
        for(unsigned int i = 0 ; i < sbs.data.size()-1 ; ++i){
            os << std::bitset<32>(sbs.data[i]);
        }
        os << std::bitset<32>(sbs.data[sbs.data.size()-1] & sbs.mask);
    }
    return os;
}


std::vector<BitStreamUint::BSBPtr> genRotatedSBS(
        unsigned int nbSBS,std::vector<float> probaVec,int size,unsigned int shift,unsigned int nbCommonBit, u_int32_t precisionMask){

    u_int32_t randomBitMask;
    if(nbCommonBit >= 31){
        randomBitMask = PRECISION_MAX;
    }else{
        randomBitMask= pow(2,nbCommonBit)-1;
    }
    unsigned int vecSize = ceil(size/32.);

    //Init streams
    std::vector<BitStreamUint::BSBPtr> res = std::vector<BitStreamUint::BSBPtr>(nbSBS);
    for(unsigned int i = 0 ; i < nbSBS ; ++i){
        if(probaVec[i] > 0 && probaVec[i] < 1){
            res[i] = BitStreamUint::BSBPtr(new BitStreamUint(size));
            res[i]->simpleValue = false;
            res[i]->data = std::vector<u_int32_t>(vecSize);
        }else{
            //The special probabilities are init here
            res[i] = BitStreamUint::BSBPtr(new BitStreamUint(probaVec[i],size,precisionMask));
        }

    }

    //generate random bits
    for(unsigned int i = 0 ; i < vecSize ; ++i){
        std::vector<u_int32_t> chuncks = generateRotatedBitChunck32(nbSBS,probaVec,shift,nbCommonBit,randomBitMask,precisionMask);
        for(unsigned int j = 0 ; j < nbSBS; ++j){
            if(probaVec[j] > 0 && probaVec[j] < 1){
                res[j]->data[i] = chuncks[j];
            }else{
                //the special proba are already initialized
            }
        }
    }
    return res;
}

