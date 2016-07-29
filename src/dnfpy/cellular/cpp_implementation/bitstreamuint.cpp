#include "bitstreamuint.h"
#include <assert.h>
#include "bitstreamutils.h"
#include <math.h>
#include <bitset>

BitStreamUint::BitStreamUint(unsigned int size,bool initMem):BitStream(size)
{
    this->index = 0;//by default
    this->vecSize = ceil(size/32.);
    //std::cout << "vec size " << this->vecSize << std::endl;
    //The mask will be applied to the last chunck only for decoding
    this->mask = LOW_MASK[(size-1)%32];
    //std::cout << "mask " << std::bitset<32>(this->mask) << std::endl;
    if(initMem){
        this->simpleValue = false;
        this->data = std::vector<u_int32_t>(this->vecSize);
    }else{ 
        this->simpleValue = true;
        this->value = false;
    }

    // std::cout << " masks " << std::bitset<32>(this->mask) << std::endl;
}

BitStreamUint::BitStreamUint(const BitStreamUint& sbs):BitStreamUint(sbs.size,false){
    this->simpleValue = sbs.simpleValue;
    this->index = sbs.index;
    this->mask = sbs.mask;
    this->value = sbs.value;
    this->data = std::vector<u_int32_t>(sbs.data.size());
    for(unsigned int i = 0 ; i < sbs.data.size(); ++i){
        this->data[i] = sbs.data[i];
    }
}


BitStreamUint::BitStreamUint(float proba,unsigned int size,u_int32_t probaMask):BitStreamUint(size,false){
    if(proba >= 1. or proba <= 0.){
        this->simpleValue = true;
        this->value = proba >= 1.0;
    }else{ //proba is not simple
        this->simpleValue = false;
        this->data = std::vector<u_int32_t>(this->vecSize);
        for(unsigned int i = 0 ; i < this->vecSize-1 ; ++i){
            this->data[i] = generateBitChunck32(proba,probaMask,32);
            //std::cout << std::bitset<32>(this->data[i]) << std::endl;
        }
        //std::cout << "SIZE : " << this->size << std::endl ;
        this->data[this->vecSize-1] = generateBitChunck32(proba,probaMask,(this->size-1)%32+1);
        //std::cout << std::bitset<32>(this->data[this->vecSize-1]) << std::endl;
    }
}

void BitStreamUint::setIndex(int index){
    this->index = index;
}
int BitStreamUint::getIndex(){
    return this->index;
}

/**switch on one of the 32 bits randomly**/
u_int32_t getRandBit32(){
    int index = rand() % 32;
    return ONE_BIT[index];

}

BitStreamUint BitStreamUint::applyCounter(const unsigned int threshold, const unsigned int size){
    BitStreamUint res = BitStreamUint(size,true);
    //TODO for now we simplify the computation by applying the threshold to chunck
    for(unsigned int i = 0 ; i < this->data.size()-1 ; ++i){
        if(__builtin_popcount(this->data[i]) > threshold){
            res.data[i] = getRandBit32();
        }        
    }
    //last chunk: we apply mask
    if( __builtin_popcount(this->data[this->data.size()-1] & this->mask) > threshold){
        res.data[this->data.size()-1] = getRandBit32();
    }
    return res;
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
    this->index = sbs.index;
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

u_int32_t BitStreamUint::rotatedChunck(const BitStreamUint &sbs,unsigned int chunckIndex, unsigned int shift) const{
    u_int32_t result;

        unsigned int chk1 = (shift / 32 + chunckIndex)%sbs.data.size();
        unsigned int chk2 = (chk1 + 1) % sbs.data.size();
        u_int32_t i32 = shift%32;
        //exemple for i32 = 2
        //111111111100 mask 1  HIGH_MASK[29]
        //000000000011 mask 2  LOW_MASK[1]
        u_int32_t mask1 = HIGH_MASK[32-1-i32]; //low bits
        u_int32_t mask2 = LOW_MASK[i32-1];//high bit

        //std::cout << "mask 1 " << std::bitset<32>(mask1) << std::endl;
        //std::cout << "mask 2 " << std::bitset<32>(mask2) << std::endl;

        u_int32_t res1 = (sbs.data[chk1] & mask1) >> i32;
        u_int32_t res2 = (sbs.data[chk2] & mask2) << (32 - i32);
        //std::cout << std::bitset<32>(res1) << std::endl;
        //std::cout << std::bitset<32>(res2) << std::endl;

        result = res1 | res2;
        //TODO finish

        return result;



} 


BitStreamUint BitStreamUint::operator<< (const unsigned int shift) const{
    //TODO finish
    if(this->simpleValue){
        //will not change the value
        return BitStreamUint(*this);
    }else{
        BitStreamUint res = BitStreamUint(this->size,true);
        for(unsigned int i = 0 ; i < this->data.size() ; ++i){

        }
        
        return res;
    }

}




BitStreamUint operator&(const BitStreamUint &right, const BitStreamUint &left){
    if(right.simpleValue){
        if(right.value)
            return BitStreamUint(left);
        else
            return BitStreamUint(0.0f,right.size);
    }else if(left.simpleValue){
        if(left.value)
            return BitStreamUint(right);
        else
            return BitStreamUint(0.0f,right.size);
    }else{

        BitStreamUint res = BitStreamUint(right.size,true);
        for(unsigned int i = 0 ; i < right.data.size() ; ++i){
            res.data[i] = right.data[i] & left.data[i];
        }
        return res;
    }
}

BitStreamUint operator|(const BitStreamUint &right, const BitStreamUint &left){
    if(right.simpleValue){
        if(right.value)
            return BitStreamUint(1.0f,right.size);
        else
            return BitStreamUint(left);
    }else if(left.simpleValue){
        if(left.value)
            return BitStreamUint(1.0f,right.size);
        else
            return BitStreamUint(right);
    }else{
        BitStreamUint res = BitStreamUint(right.size,true);
        for(unsigned int i = 0 ; i < right.data.size() ; ++i){
            res.data[i] = right.data[i] | left.data[i];
        }
        return res;
    }
}



BitStreamUint operator^(const BitStreamUint &right, const BitStreamUint &left){
    if(right.simpleValue){
        if(right.value) // 1 xor left gives ~left
            return ~left;
        else //0 xor left gives left
            return BitStreamUint(left);
    }else if(left.simpleValue){
        if(left.value) //1 xor right give ~right
            return ~right;
        else// 0 xor right gives right
            return BitStreamUint(right);
    }else{
        BitStreamUint res = BitStreamUint(right.size,true);
        for(unsigned int i = 0 ; i < right.data.size() ; ++i){
            res.data[i] = right.data[i] ^ left.data[i];
        }
        return res;
    }
}

BitStreamUint operator+(const BitStreamUint &right, const BitStreamUint &left){
    BitStreamUint res = BitStreamUint(right.size,true);//force creation of data
    BitStreamUint rand = BitStreamUint(0.5,right.size); //sel bit
    for(unsigned int i = 0 ; i < right.data.size() ; ++i){
        res.data[i] = (right.data[i]&rand.data[i]) | (left.data[i]&(~rand.data[i]));
    }
    return res;
}

BitStreamUint operator~(const BitStreamUint &bs){
    if(bs.simpleValue){
        return BitStreamUint(not(bs.value),bs.size);
    }else{
        BitStreamUint res = BitStreamUint(bs.size,true);
        for(unsigned int i = 0 ; i < bs.data.size() ; ++i){
            res.data[i] = ~bs.data[i];
        }
        return res;
    }
}

/**
 *Return a 32b chunck of bits from the bitstream starting from index
 *mask the last chunck using this->mask
 * If this->index = 0 return this->data[chunckIndex] (fast)
 * access is wrapped so as any stream can be processed against any other stream
 * even if the size is different
 * 
 */
u_int32_t BitStreamUint::getData(unsigned int chunckIndex) const{
    u_int32_t result;
    unsigned int chkI = chunckIndex % this->data.size();
    if(this->index == 0){
        if(chkI == this->data.size()-1)
            result = this->data[chkI] & this->mask;
        else
            result = this->data[chkI];
    }else{
        assert(false); //NOT IMPLEMENTED
    }

    return result;

}


std::ostream& operator<< (std::ostream &os, const BitStreamUint& sbs){
    if(sbs.simpleValue){
        os << sbs.value;
    }else{
        for(unsigned int i = 0 ; i < sbs.data.size() ; ++i){
            os << std::bitset<32>(sbs.getData(i));
        }
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

