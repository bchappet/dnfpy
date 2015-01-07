#ifndef REGISTER_H
#define REGISTER_H


class IRegister
{
public:
    virtual void synch() = 0;
    virtual void reset() = 0;


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
    virtual void synch() override;
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

    /**
     * @brief reset get back to initState
     */
    virtual void reset() override;
private:
    T initState;
    T nextState;
    T state;
};

#endif // REGISTER_H
