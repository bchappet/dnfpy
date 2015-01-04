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

    virtual void cellConnection(Module* cell,Module* neighCell,int dir)const{
        if(neighCell!=nullptr){
            cell->addInput(neighCell);
        }
    }

    virtual void connect(int width,int height,Module*** cellArray) const override{

        std::vector<Module*> inputs;
        for(int i = 0 ; i < height ; i++){
            for(int j = 0 ; j < width ; j++){
                Module* cell = cellArray[i][j];
                inputs.clear();
                if(this->within_border(i-1,j,height,width))
                    this->cellConnection(cell,cellArray[i-1][j],N);
                else
                    this->cellConnection(cell,nullptr,N);

                if(this->within_border(i+1,j,height,width))
                    this->cellConnection(cell,cellArray[i+1][j],S);
                else
                    this->cellConnection(cell,nullptr,S);

                if(this->within_border(i,j+1,height,width))
                    this->cellConnection(cell,cellArray[i][j+1],E);
                else
                    this->cellConnection(cell,nullptr,E);

                if(this->within_border(i,j-1,height,width))
                    this->cellConnection(cell,cellArray[i][j-1],W);
                else
                    this->cellConnection(cell,nullptr,W);


            }
        }
    }

};



#endif // NeumannCONNECTER_H
