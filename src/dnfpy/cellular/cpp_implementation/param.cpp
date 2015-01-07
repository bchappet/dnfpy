#include "param.h"

template<typename T>
Param<T>::Param(T initVal)
{
    this->val = initVal;
    this->initVal = initVal;
}

template<typename T>
void Param<T>::reset(){
    this->val = this->initVal;
}

template class Param<int>;
template class Param<float>;
template class Param<bool>;
