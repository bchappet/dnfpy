#ifndef PARAM_H
#define PARAM_H

class IParam{
public:
    virtual void reset() = 0;
};

template<typename T>
class Param: public IParam
{
public:
    Param(T initVal);
    virtual void reset() override;
    T val;
private:
    T initVal;
};

#endif // PARAM_H
