#ifndef CONNECTER_H
#define CONNECTER_H
#include "module.h"
class Connecter{
public:
    Connecter(){}

    virtual void connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray) const = 0;

protected:
    bool within_border(int i,int j,int height,int width) const{
        return i >= 0 && j >= 0 && i < height && j < width;
    }
};

#endif // CONNECTER_H
