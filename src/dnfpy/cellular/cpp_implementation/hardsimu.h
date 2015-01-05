#ifndef HARDSIMU_H
#define HARDSIMU_H
#include <string>
/**
 * Interface for distributed cellular array simulation
 * @brief The HardSimu class
 */
class HardSimu
{
public:
    HardSimu(){

    }
    /**
     * @brief step Perform one step of siimulation
     */
    virtual void step() = 0;

    /**
     * @brief getArrayInt return an 2D array of int using the cells of the map
     * @param code
     * @return
     */
    virtual void getArrayInt(int index,int** array) =0;

    virtual void getArrayBool(int index,bool ** array) =0;

    virtual void getArrayFloat(int index,float ** array) =0;

     /** @brief setArrayInt will give an integer to each cell.
     * The cell will deal with it according to the code
     * @param array
     * @param code
     */
    virtual void setArrayInt(int index, int** array) = 0;

    virtual void setArrayBool(int index, bool** array) = 0;

    virtual void setArrayFloat(int index, float** array) = 0;

    virtual void setCellInt(int x,int y,int index,int val) = 0;
    virtual void setCellBool(int x,int y,int index,bool val) = 0;
    virtual void setCellFloat(int x,int y,int index,float val) = 0;

    /**
     * @brief nstep perform n step of simulation
     * @param n
     */
    void nstep(int n)
    {
        for(int i = 0 ; i < n ; i++){
            this->step();
        }
    }



};

#endif // HARDSIMU_H
