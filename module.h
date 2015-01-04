#ifndef CELL_H
#define CELL_H
#include "register.h"
#include <vector>
#include "param.h"

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

    void addInputs(std::vector<Module*> new_inputs){
        this->inputs.insert(this->inputs.end(),new_inputs.begin(),new_inputs.end());
    }

    void addInput(Module* input){
        this->inputs.push_back(input);
    }

    template <typename T>
    void setRegState(int index,T val){
        this->getReg<T>(index)->set(val);
    }

    template <typename T>
    T getRegState(int index){
        return this->getReg<T>(index)->get();
    }


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

    Module* getInput(int index){
        return this->inputs.at(index);
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

protected:
    std::vector<IRegister*> regs;//inner state of the module
    std::vector<Module*> inputs;
    std::vector<Module*> subModules;

    std::vector<IParam*> params;//parameters of the module for experimentation

private:
    template <typename T>
    Register<T>* getReg(int index){
        return (Register<T>*)(this->regs.at(index));
    }

};

#endif // CELL_H
