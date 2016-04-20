#ifndef REGISTER_H
#define REGISTER_H




class Register
{
public:
    /**
     * @brief Register init state and next state with val
     * @param val
     * @param size : number of bit of this register. No size check is done for now.
     */
    Register(const int& val,const int size=16);


    enum ErrorType {TRANSIENT,PERMANENT_HIGH,PERMANENT_LOW};

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
     * utility function to increment or decrement easyly
     */
    void incr(int toAdd);

    /**
     * Return the size of the register
     */
    int getSize();

    /**
     * Set the error mask msb -> lsb
     */
    void setErrorMask(int errorMask,ErrorType errorType);

    /**
     * @brief set the error mask from a bool array
     * msb -> lsb
     * return a pointer to the next unused bool
     */
    bool* setErrorMaskFromArray(bool * bits,ErrorType errorType);

    int getErrorMask(ErrorType errorType);
    /**
     * @brief reset get back to initState
     */
    void reset();
private:
    int initState;
    int nextState;
    int state;
    int size;
    int transientErrorMask; //state = nextState ^ errorMask then is 0
    int permanentHigh; //state = nextState | permanentHigh
    int permanentLow;  //state = nextState & permanentLow
};

#endif // REGISTER_H
