#include "neumannconnecter.h"

void NeumannConnecter::cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const{
    if(neighCell!=nullptr){
        cell->addNeighbour(neighCell);
    }
}


void NeumannConnecter::connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray) const{


    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
            Module::ModulePtr cell = cellArray[i][j];
            this->cellConnection(cell);
            if(this->within_border(i-1,j,height,width))
                this->cellNeighbourConnection(cell,cellArray[i-1][j],N);
            else
                this->cellNeighbourConnection(cell,nullptr,N);

            if(this->within_border(i+1,j,height,width))
                this->cellNeighbourConnection(cell,cellArray[i+1][j],S);
            else
                this->cellNeighbourConnection(cell,nullptr,S);

            if(this->within_border(i,j+1,height,width))
                this->cellNeighbourConnection(cell,cellArray[i][j+1],E);
            else
                this->cellNeighbourConnection(cell,nullptr,E);

            if(this->within_border(i,j-1,height,width))
                this->cellNeighbourConnection(cell,cellArray[i][j-1],W);
            else
                this->cellNeighbourConnection(cell,nullptr,W);


        }
    }
}

