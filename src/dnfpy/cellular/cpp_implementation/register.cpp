#include "register.h"


/**
 * @brief Register init state and next state with val
 * @param val
 */
template <typename T>
Register<T>::Register(const T& val){
    this->state = val;
    this->nextState = val;
    this->initState = val;
}

template <typename T>
void Register<T>::reset(){
    this->state = initState;
    this->nextState = initState;
}

/**
 * @brief synch state = nextState
 */
template <typename T>
void Register<T>::synch(){
    this->state = nextState;
}

/**
 * @brief get the state
 * @return
 */
template <typename T>
T Register<T>::get(){
    return this->state;
}



/**
 * @brief set the nextState
 * @param val
 */
template <typename T>
void Register<T>::set(T val){
    this->nextState = val;
}

template class Register<int>;
template class Register<bool>;
template class Register<float>;
