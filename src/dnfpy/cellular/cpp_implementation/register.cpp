#include "register.h"
#include <vector>

/**
 * @brief Register init state and next state with val
 * @param val
 */

Register::Register(const int& val,const int size){
    this->state = val;
    this->nextState = val;
    this->initState = val;
    this->size = size;
    this->errorMask = 0;
}


void Register::reset(){
    this->state = initState;
    this->nextState = initState;
}

/**
 * @brief synch state = nextState
 */

void Register::synch(){
    this->state = nextState ^ errorMask;
}

/**
 * @brief get the state
 * @return
 */

int Register::get(){
    return this->state;
}

int Register::getSize(){
    return this->size;
}


void Register::setErrorMask(int errorMask){
    this->errorMask = errorMask;
}

bool *  Register::setErrorMaskFromArray(bool * bits){
    this->errorMask = 0;
    bool * bit = bits;
    for( int i = this->size-1 ; i >= 0 ; --i){
        this->errorMask = this->errorMask | (*(bit) << i);
        bit++;
    }
    return bit;
}

int Register::getErrorMask(){
    return this->errorMask;
}

/**
 * @brief set the nextState
 * @param val
 */

void Register::set(int val){
    this->nextState = val;
}

