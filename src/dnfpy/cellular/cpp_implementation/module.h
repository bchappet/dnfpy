#ifndef CELL_H
#define CELL_H
#include "register.h"
#include <vector>
#include "param.h"
#include <assert.h>
#include <iostream>
#include<boost/ptr_container/ptr_vector.hpp>
#include <boost/shared_ptr.hpp>



class Module
{

public:
    typedef boost::shared_ptr<Module> ModulePtr;
    typedef boost::shared_ptr<std::vector<void*>> ParamsPtr;

    Module(){}

    /**
     * @brief preCompute optional and not recursif: is not called on the submodules
     */
    virtual void preCompute(){}

    virtual void compute(){
        for(unsigned int i = 0; i < this->subModules.size() ; i++){

            this->subModules[i].get()->compute();
        }
        this->computeState();
    }

    void setParams(ParamsPtr params){
        this->params = params;
        for(ModulePtr mod : this->subModules){
            mod.get()->setParams(params);
        }
    }

    virtual void computeState(){}

    /**
     * Should be called only once per map2D
     * @brief getDefaultParams
     * @return
     */
    virtual void setDefaultParams(ParamsPtr params){}




    void addNeighbours(std::vector<ModulePtr> &new_neighbours){
        this->neighbours.insert(this->neighbours.end(),new_neighbours.begin(),new_neighbours.end());
    }

    /**
     * @brief addNeighbour
     * @param input
     */
    void addNeighbour(ModulePtr input){
        this->neighbours.push_back(input);
    }


    void setRegState(int index,int val){
        this->regs.at(index).set(val);
    }


    int getRegState(int index){
        return this->regs.at(index).get();
    }

    virtual void getAttribute(int index,void* value){}

    virtual void setAttribute(int index, void* value){}


    virtual void synch(){

        for(unsigned int i = 0; i < this->subModules.size() ; i++){
            subModules[i].get()->synch();
        }
        for(unsigned int i = 0; i < this->regs.size() ; i++){
            this->regs[i].synch();
        }

    }

    size_t getSubModuleCount(){
        return this->subModules.size();
    }

    void setSubModuleState(int subModuleIndex,int regIndex,int value){
        this->subModules[subModuleIndex].get()->setRegState(regIndex,value);
    }

    int getSubModuleState(int subModuleIndex,int regIndex){
        return this->subModules[subModuleIndex].get()->getRegState(regIndex);
    }


    ModulePtr getSubModule(int index){
        //std::cout << "getting sub module" << index << std::endl;
        return this->subModules.at(index);
    }

    std::vector<ModulePtr> getSubModules(){
        return this->subModules;
    }

    ModulePtr getNeighbour(int index){
        return this->neighbours.at(index);
    }

    template<typename T>
    void setParam(int index,T value){

        *((T*)this->params->at(index)) = value;
    }


    template <typename T> T getParam(int index){
       // std::cout << "size params : " << this->params->size() << std::endl;
        //std::cout << "getting param " << index << std::endl;
        return *((T*)this->params->at(index));
    }


    /**
     * @brief reset the register and the submodules
     */
    virtual void reset(){
        for(unsigned int i = 0; i < this->subModules.size() ; ++i){
            this->subModules[i]->reset();
        }
        for(unsigned int i = 0; i < this->regs.size() ; i++){
            this->regs[i].reset();
        }
    }

protected:
    std::vector<Register> regs;//inner state of the module
    std::vector<ModulePtr> neighbours;
    std::vector<ModulePtr> subModules;
    ParamsPtr params;//only one instance will be constructed : in the map





};

#endif // CELL_H
