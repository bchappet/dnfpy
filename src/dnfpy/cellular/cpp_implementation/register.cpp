#include "register.h"
#include <iostream>
#include <vector>
#include "bitstreamutils.h"

/**
 * @brief Register init state and next state with val
 * @param val
 */

Register::Register(const int& val,const int size){
    this->precisionMask = LOW_MASK[size-1];
    this->state = val & this->precisionMask;
    this->nextState = val & this->precisionMask;
    this->initState = val & this->precisionMask;
    this->size = size;
    this->transientErrorMask = 0;
    this->permanentHigh = 0;
    this->permanentLow = 0;
}


void Register::reset(){
    this->state = initState;
    this->nextState = initState;
}

/**
 * @brief synch state = nextState
 */

void Register::synch(){
    this->state = this->nextState ^ this->transientErrorMask;
    this->state = this->state | this->permanentHigh;
    this->state = this->state & (~this->permanentLow);
    this->nextState = this->state; //by default
}

/**
 * @brief get the state
 * @return
 */

int Register::get(){
    return this->state;
}

void Register::incr(int toAdd){
    this->set(this->get() + toAdd);
}

int Register::getSize(){
    return this->size;
}


void Register::setErrorMask(int errorMask,Register::ErrorType errorType){
    switch(errorType){
        case TRANSIENT : this->transientErrorMask = errorMask;break;
        case PERMANENT_HIGH : this->permanentHigh = errorMask;break;
        case PERMANENT_LOW : this->permanentLow = errorMask;break;
    }
}

bool *  Register::setErrorMaskFromArray(bool * bits,Register::ErrorType errorType){
    int errorMask = 0;
    bool * bit = bits;
    for( int i = this->size-1 ; i >= 0 ; --i){
        errorMask = errorMask | (*(bit) << i);
        bit++;
    }
    this->setErrorMask(errorMask,errorType);
    return bit;
}

int Register::getErrorMask(Register::ErrorType errorType){
    switch(errorType){
        case TRANSIENT :return this->transientErrorMask;
        case PERMANENT_HIGH :return this->permanentHigh;
        case PERMANENT_LOW : return this->permanentLow;
        default: std::cout << "errorType " << errorType << " does not exist" <<std::endl;return -1;
    }
}

/**
 * @brief set the nextState
 * @param val
 */

void Register::set(int val){
    this->nextState = val & this->precisionMask;
}

