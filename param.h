#ifndef PARAM_H
#define PARAM_H

class IParam{

};

template<typename T>
class Param: public IParam
{
public:
    Param(T initVal);
    T val;
};

#endif // PARAM_H
