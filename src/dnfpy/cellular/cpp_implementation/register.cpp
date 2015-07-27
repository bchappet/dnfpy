#include "register.h"
#include <vector>

/**
 * @brief Register init state and next state with val
 * @param val
 */

Register::Register(const int& val){
    this->state = val;
    this->nextState = val;
    this->initState = val;
}


void Register::reset(){
    this->state = initState;
    this->nextState = initState;
}

/**
 * @brief synch state = nextState
 */

void Register::synch(){
    this->state = nextState;
}

/**
 * @brief get the state
 * @return
 */

int Register::get(){
    return this->state;
}



/**
 * @brief set the nextState
 * @param val
 */

void Register::set(int val){
    this->nextState = val;
}

