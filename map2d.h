#ifndef MAP2D_H
#define MAP2D_H
#include "module.h"
#include "connecter.h"
#include <typeinfo>
#include <iostream>
#include <string>


class Map2D : public Module
{
public:

    /**
     * @brief Map construct a width*heigth map of module
     * @param width
     * @param height
     */
    Map2D(int width,int height);


    /**
     * @brief initCellArray : init cell array with given module
     */
    template <class M>
    void initCellArray(){
        std::cout << "init cell of size " << this->heigth <<"," << this->width << std::endl;
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j] = new M();
            }
        }
    }

    virtual void compute() override;

    virtual void synch() override;

    /**
     * @brief getCellState return the state of a cell at x,y
     * @param x
     * @param y
     * @return
     */
    template <typename T>
    T getCellState(int x,int y,int index){
         return this->cellArray[y][x]->getRegState<T>(index);
    }

    /**
     * @brief setCellState set a pecific cell state at x,y
     * @param x
     * @param y
     * @param val
     */
    template <typename T>
    void setCellState(int x,int y,int index,T val){
        this->cellArray[y][x]->setRegState<T>(index,val);
    }

    /**
     * @brief getArrayState
     * @param index
     * @return
     */
    template <typename T>
    void getArrayState(int index,T** array){


        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                array[i][j] = this->cellArray[i][j]->getRegState<T>(index);
            }
        }
    }

    /**
     * @brief setArrayState
     * @param index
     * @param val
     */
    template <typename T>
    void setArrayState(int index,T** arrayVal){
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j]->setRegState<T>(index,arrayVal[i][j]);
            }
        }
    }

    /**
     * @brief setParamArray set param off every cell of the array
     * @param index
     * @param value
     */
    template<typename T>
    void setParamArray(int index,T value){
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j]->setParam(index,value);
            }
        }
    }

    /**
     * @brief setParamArrayPath to set params deeper in the modules
     * @param index
     * @param value
     * @param path TODO "submoduleIndex/subModuleIndex" ..
     * for instance "0..1/1
     * of 1/\* etc
     * FOR NOW it is only working for \*
     */
    template<typename T>
    void setParamArrayPath(int index,T value,std::string path){
        if(path.compare("*") != 0){
            std::cout << "onl y * available for now" << std::endl;
        }
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                for(Module* child : this->cellArray[i][j]->getSubModules())
                    child->setParam<T>(index,value);
            }
        }
    }

    /**
     * @brief connect the cell together and the cell sub module to input cell submodules
     * if cellC is provided
     * @param c
     * @param cellC
     */
    void connect(const Connecter& c){
        c.connect(this->width,this->heigth,this->cellArray);
    }



protected:
    int width;
    int heigth;
    Module*** cellArray;

};

#endif // MAP2D_H
