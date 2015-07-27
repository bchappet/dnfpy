#ifndef REGISTER_H
#define REGISTER_H




class Register
{
public:
    /**
     * @brief Register init state and next state with val
     * @param val
     */
    Register(const int& val);
    /**
     * @brief synch state = nextState
     */
    void synch() ;
    /**
     * @brief get the state
     * @return
     */
    int get();



    /**
     * @brief set the nextState
     * @param val
     */
    void set(int val);

    /**
     * @brief reset get back to initState
     */
    void reset();
private:
    int initState;
    int nextState;
    int state;
};

#endif // REGISTER_H
