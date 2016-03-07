#ifndef NeumannCONNECTER_H
#define NeumannCONNECTER_H


#include "connecter.h"
#include <vector>
#include <iostream>
#include <assert.h>

class NeumannConnecter : public Connecter
{
public:
    enum NeumannDirection { N,S,E,W} ;
    NeumannConnecter(){}

    virtual void cellConnection(Module::ModulePtr cell) const{}

    virtual void cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const;

    virtual void connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray,bool wrap = false) const override;

};



#endif // NeumannCONNECTER_H
