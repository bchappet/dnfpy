#ifndef MAP2D_H
#define MAP2D_H
#include "module.h"
#include "connecter.h"
#include <typeinfo>
#include <iostream>
#include <string>
#include<boost/ptr_container/ptr_vector.hpp>


class Map2D : public Module
{
public:

    Map2D();

    /**
     * @brief Map construct a width*heigth map of module
     * @param width
     * @param height
     */
    Map2D(int width,int height);

    ~Map2D();

    void initMemory(int width,int height);

    /**
     * @brief initCellArray : init cell array with given module
     */
    template <class M>
    void initCellArray(){

        //std::cout << "init cell of size " << this->heigth <<"," << this->width << std::endl;
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j] = Module::ModulePtr(new M());
                this->cellArray[i][j]->setParams(this->params);
            }
        }
        this->cellArray[0][0]->setDefaultParams(this->params);


    }

    /**
     * @brief initCellArray : init cell array with given module and a given parameter
     */
    template <class M>
    void initCellArray(std::string param){

        //std::cout << "init cell of size " << this->heigth <<"," << this->width << std::endl;
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j] = Module::ModulePtr(new M(param));
                this->cellArray[i][j]->setParams(this->params);

            }
        }
        this->cellArray[0][0]->setDefaultParams(this->params);
    }

    virtual void preCompute() override;

    virtual void compute() override;

    virtual void synch() override;

    virtual void reset() override;

    void initMapSeed(long int seed);



    /**
             * @brief getCellAttribute to access attribute of cells
             * @param x
             * @param y
             * @param index
             * @param value
             */
    void getCellAttribute(int x,int y,int index,void* value);

    void setCellAttribute(int x,int y,int index, void* value);


    template <typename T>
    void getArrayAttribute(int index, T* array){
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j]->getAttribute(index,array +(i*this->width + j));
                // std::cout << "(" << i << "," << j << "):" << *(int*)(array +(i*this->width + j)) <<  std::endl;
            }
        }
    }
    template <typename T>
    void setArrayAttribute(int index, T* array){
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j]->setAttribute(index,array +(i*this->width + j));
            }
        }
    }



    /**
             * @brief getCellState return the state of a cell at x,y
             * @param x
             * @param y
             * @return
             */

    int getCellState(int x,int y,int index){
        return this->cellArray[y][x]->getRegState(index);
    }

    /**
             * @brief setCellState set a pecific cell state at x,y
             * @param x
             * @param y
             * @param val
             */

    void setCellState(int x,int y,int index,int val){
        this->cellArray[y][x]->setRegState(index,val);
    }

    /**
             * @brief getArrayState
             * @param index
             * @return
             */
    void getArrayState(int index,int* array){


        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                array[i*this->width + j] = this->cellArray[i][j]->getRegState(index);
            }
        }
    }

    /**
             * @brief setArrayState
             * @param index
             * @param val
             */
    void setArrayState(int index,int* array){
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j]->setRegState(index,array[i*this->width + j]);
            }
        }
    }




    /**
             * @brief getMapParam return the param using path for first cell.
             * As all the param should be the same, it is relevant
             * @param index
             * @param path
             */
    void* getMapParam(int index){
        return this->params->at(index);
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

    Module::ModulePtr getCell(int x,int y){
        return this->cellArray[y][x];
    }


protected:

    int width;
    int heigth;
    std::vector<std::vector<Module::ModulePtr>> cellArray;


};

#endif // MAP2D_H
