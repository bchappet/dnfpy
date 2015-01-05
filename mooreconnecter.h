#ifndef MooreCONNECTER_H
#define MooreCONNECTER_H
#include "connecter.h"
#include <vector>
#include <iostream>
#include <assert.h>

class MooreConnecter : public Connecter
{
public:
    enum MooreDirection { NW,N,NE,W,E,SW,S,SE} ;
    MooreConnecter(){}

    virtual void cellConnection(Module* cell,Module* neighCell,int dir)const;

    virtual void connect(int width,int height,Module*** cellArray) const override;

};

#endif // MooreCONNECTER_H
