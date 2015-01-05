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

    virtual void cellConnection(Module* cell,Module* neighCell,int dir)const;

    virtual void connect(int width,int height,Module*** cellArray) const override;

};



#endif // NeumannCONNECTER_H
