#ifndef CELL_H
#define CELL_H
#include "register.h"
#include <vector>

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

    Module* getInput(int index){
        return this->inputs.at(index);
    }

protected:
    std::vector<IRegister*> regs;//inner state of the module
    std::vector<Module*> inputs;
    std::vector<Module*> subModules;

private:
    template <typename T>
    Register<T>* getReg(int index){
        return static_cast<Register<T>*>(this->regs.at(index));
    }

};

#endif // CELL_H
