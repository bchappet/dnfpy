#ifndef REGISTER_H
#define REGISTER_H


class IRegister
{
public:
    virtual void synch() = 0;



};


template <typename T>
class Register:public IRegister
{
public:
    /**
     * @brief Register init state and next state with val
     * @param val
     */
    Register(const T& val);
    /**
     * @brief synch state = nextState
     */
    void synch();
    /**
     * @brief get the state
     * @return
     */
    T get();



    /**
     * @brief set the nextState
     * @param val
     */
    void set(T val);
private:
    T nextState;
    T state;
};

#endif // REGISTER_H
