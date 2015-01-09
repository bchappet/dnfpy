#ifndef CELL_H
#define CELL_H
#include "register.h"
#include <vector>
#include "param.h"
#include <assert.h>
#include <iostream>

class Module
{
public:

    Module(){}

    virtual void compute(){
        for(Module* mod:this->subModules){
            mod->compute();
        }
        this->computeState();
    }

    virtual void computeState(){}

    /**
     * @brief linkParam will link the param of target with this param
     * Which means that
     *  1) target param value will be the same as this
     *  2) Every modification on any side will be transmitted to the other
     * @param indexParam
     * @param indexParamTarget
     * @param target
     */
    void linkParam(int indexParam,int indexParamTarget,Module* target){
        target->params[indexParamTarget] = this->params[indexParam];
//        this->setParam<float>(indexParam,0.01);
//        std::cout << "param :target" << target->getParam<float>(indexParamTarget) << std::endl;
//        assert(target->getParam<float>(indexParamTarget) < 0.01);
    }


    void addNeighbours(std::vector<Module*> new_neighbours){
        this->neighbours.insert(this->neighbours.end(),new_neighbours.begin(),new_neighbours.end());
    }

    void addNeighbour(Module* input){
        this->neighbours.push_back(input);
    }

    template <typename T>
    void setRegState(int index,T val){
        this->getReg<T>(index)->set(val);
    }

    template <typename T>
    T getRegState(int index){
        return this->getReg<T>(index)->get();
    }

    virtual void getAttribute(int index,void* value){}

    virtual void setAttribute(int index, void* value){}


    virtual void synch(){
        for(Module* mod:this->subModules){
            mod->synch();
        }
        for(IRegister* reg:this->regs){
            reg->synch();
        }

    }


    Module* getSubModule(int index){
        return this->subModules.at(index);
    }

    std::vector<Module*> getSubModules(){
        return this->subModules;
    }

    Module* getNeighbour(int index){
        return this->neighbours.at(index);
    }

    template<typename T>
    void setParam(int index, T value){
        Param<T>* param = (Param<T>*) (this->params.at(index));
        param->val = value;
    }

    template<typename T>
    T getParam(int index){
        Param<T>* param = (Param<T>*) (this->params.at(index));
        return param->val;
    }

    /**
     * @brief reset the register and the submodules
     */
    virtual void reset(){
        for(Module* mod : this->subModules){
            mod->reset();
        }
        for(IRegister* reg:this->regs){
            reg->reset();
        }

    }

protected:
    std::vector<IRegister*> regs;//inner state of the module
    std::vector<Module*> neighbours;
    std::vector<Module*> subModules;

    std::vector<IParam*> params;//parameters of the module for experimentation

private:
    template <typename T>
    Register<T>* getReg(int index){
        return (Register<T>*)(this->regs.at(index));
    }

};

#endif // CELL_H
