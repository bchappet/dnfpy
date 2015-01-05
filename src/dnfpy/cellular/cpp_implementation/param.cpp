#include "param.h"

template<typename T>
Param<T>::Param(T initVal)
{
    this->val = initVal;
}

template class Param<int>;
template class Param<float>;
template class Param<bool>;
