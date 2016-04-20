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
     * @brief Map construct a width*height map of module
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

        //std::cout << "init cell of size " << this->height <<"," << this->width << std::endl;
        for(int i = 0 ; i < this->height ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j] = Module::ModulePtr(new M(i,j));
                this->cellArray[i][j]->initParams();
                //this->cellArray[i][j]->setParams(this->params);
            }
        }
        //this->cellArray[0][0]->setDefaultParams(this->params);


    }

    /**
     * @brief initCellArray : init cell array with given module and a given parameter
     */
    template <class M>
    void initCellArray(std::string param){

        //std::cout << "init cell of size " << this->height <<"," << this->width << std::endl;
        for(int i = 0 ; i < this->height ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j] = Module::ModulePtr(new M(i,j,param));
                this->cellArray[i][j]->initParams();
                //this->cellArray[i][j]->setParams(this->params);
            }
        }
        //this->cellArray[0][0]->setDefaultParams(this->params);
    }

    virtual void preCompute() override;

    virtual void compute() override;

    virtual void synch() override;

    virtual void reset() override;

    void initMapSeed(long int seed);



    int getCellReg(int x,int y,int index);

    void setCellReg(int x,int y,int index, int value);



    virtual int getTotalRegSize() override;
    virtual bool* setErrorMaskFromArray(bool * bits,Register::ErrorType errorType) override;

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
        for(int i = 0 ; i < this->height ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j]->getAttribute(index,array +(i*this->width + j));
                // std::cout << "(" << i << "," << j << "):" << *(int*)(array +(i*this->width + j)) <<  std::endl;
            }
        }
    }
    template <typename T>
    void setArrayAttribute(int index, T* array){
        for(int i = 0 ; i < this->height ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j]->setAttribute(index,array +(i*this->width + j));
            }
        }
    }



    template < typename T>
    T getCellParam(int x,int y,int index){
        return this->cellArray[y][x]->getParam<T>(index);
    }

    template < typename T>
    T getCellSubParam(int x,int y,int z,int index){
        return this->cellArray[y][x]->getSubModule(z)->getParam<T>(index);
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
        for(int i = 0 ; i < this->height ; i++){
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
        for(int i = 0 ; i < this->height ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j]->setRegState(index,array[i*this->width + j]);
            }
        }
    }


    void setArraySubState(int regIndex,int* array){
        size_t subModuleCount = this->cellArray[0][0]->getSubModuleCount();
        for(int i = 0 ; i < this->height ; ++i){
            for( int j = 0 ; j < this->width ; ++j){
                for(size_t k = 0 ; k < subModuleCount ; ++k){
                    this->cellArray[i][j]->setSubModuleState(k,regIndex,array[i*(this->width*subModuleCount) + j*subModuleCount + k]);
                }
            }
        }
    }

    void getArraySubState(int regIndex,int* array){
        size_t subModuleCount = this->cellArray[0][0]->getSubModuleCount();
        for(int i = 0 ; i < this->height ; ++i){
            for( int j = 0 ; j < this->width ; ++j){
                for(size_t k = 0 ; k < subModuleCount ; ++k){
                    array[i*(this->width*subModuleCount) + j*subModuleCount + k] = this->cellArray[i][j]->getSubModuleState(k,regIndex);
                }
            }
        }
    }


    /**
     * @brief set the *same* param for all the array
     */
    template <typename T>
    void setArrayParam(int paramIndex,T value){
        for(int i = 0 ; i < this->height ; ++i){
            for(int j = 0 ; j < this->width ; ++j){
                this->cellArray[i][j]->setParam<T>(paramIndex,value);
            }
        }
    }

    /**
     * @brief set the *same* param for all the array sub modules
     */
    template <typename T>
    void setArraySubParam(int paramIndex,T value){
        size_t subModuleCount = this->cellArray[0][0]->getSubModuleCount();
        for(int i = 0 ; i < this->height ; ++i){
            for(int j = 0 ; j < this->width ; ++j){
                for(size_t k = 0 ; k < subModuleCount ; ++k){
                    Module::ModulePtr mod = this->cellArray[i][j]->getSubModule(k);
                    mod->setParam<T>(paramIndex,value);
                }
            }
        }
    }




    /**
    * @brief getMapParam return the param using path for first cell.
    * As all the param should be the same, it is relevant
    * @param index
    * @param path
    */
    //void* getMapParam(int index){
    //    return this->params->at(index);
    //}

    /**
    * @brief connect the cell together and the cell sub module to input cell submodules
    * @param c
    */
  void connect(const Connecter& c,bool wrap=false){
        c.connect(this->width,this->height,this->cellArray,wrap);
    }

    Module::ModulePtr getCell(int x,int y){
        return this->cellArray[y][x];
    }


protected:

    int width;
    int height;
    std::vector<std::vector<Module::ModulePtr>> cellArray;


};

#endif // MAP2D_H
