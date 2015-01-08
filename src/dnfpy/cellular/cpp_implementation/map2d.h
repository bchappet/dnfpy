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

    Map2D();
    /**
     * @brief Map construct a width*heigth map of module
     * @param width
     * @param height
     */
    Map2D(int width,int height);

    void initMemory(int width,int height);

    /**
     * @brief initCellArray : init cell array with given module
     */
    template <class M>
    void initCellArray(){
        //std::cout << "init cell of size " << this->heigth <<"," << this->width << std::endl;
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j] = new M();
            }
        }
    }

    virtual void compute() override;

    virtual void synch() override;

    virtual void reset() override;

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
    void getArrayState(int index,T* array){


        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                array[i*this->width + j] = this->cellArray[i][j]->getRegState<T>(index);
            }
        }
    }

    /**
     * @brief setArrayState
     * @param index
     * @param val
     */
    template <typename T>
    void setArrayState(int index,T* array){
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                this->cellArray[i][j]->setRegState<T>(index,array[i*this->width + j]);
            }
        }
    }


    std::vector<Module*> getModulesFromPath(Module* cell,std::string path){
        std::vector<Module*> modules;
        if(path.compare(".") == 0){
            modules.push_back(cell);
        }else if(path.compare("./*") == 0){
            for(Module* child : cell->getSubModules())
                modules.push_back(child);
        }else{
            std::cout << "onl y \".\" and \"./*\"  available for now" << std::endl;
        }
        return modules;
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
    void setMapParam(int index,T value,std::string path="."){
        for(int i = 0 ; i < this->heigth ; i++){
            for(int j = 0 ; j < this->width ; j++){
                for(Module* mod : this->getModulesFromPath(this->cellArray[i][j],path))
                    mod->setParam<T>(index,value);
            }
        }
    }

    /**
     * @brief getMapParam return the param using path for first cell.
     * As all the param should be the same, it is relevant
     * @param index
     * @param path
     */
    template<typename T>
    T getMapParam(int index,std::string path="."){
        Module* mod = this->getModulesFromPath(this->cellArray[0][0],path).at(0);
        return mod->getParam<T>(index);
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

    Module* getCell(int x,int y){
        return this->cellArray[y][x];
    }


protected:

    int width;
    int heigth;
    Module*** cellArray;

};

#endif // MAP2D_H
