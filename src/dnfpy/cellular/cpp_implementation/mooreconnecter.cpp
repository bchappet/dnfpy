#include "mooreconnecter.h"

void MooreConnecter::cellConnection(Module* cell,Module* neighCell,int dir) const{
    if(neighCell!=nullptr){
        cell->addInput(neighCell);
    }
}

void MooreConnecter::connect(int width,int height,Module*** cellArray) const{

    std::vector<Module*> inputs;
    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
           // std::cout << "i,j: (" << i << "," << j << ")" << std::endl;
            inputs.clear();
            int dir = 0;
            for(int a = -1 ; a <= 1 ; a++){
                for(int b = -1 ; b <= 1; b++){
                    Module* cell = cellArray[i][j];
                    if(a!=0 || b!= 0){
                       // std::cout << "(" << i+a << "," << j+b << ")" << std::endl;
                        if(this->within_border(i+a,j+b,height,width)){
                           // std::cout << "passed" << std::endl;
                            this->cellConnection(cell,cellArray[i+a][j+b],dir);
                        }else{
                            //TODO wrap if needed
                            this->cellConnection(cell,nullptr,dir);
                        }
                    }
                    dir ++;
                }
            }
        }
    }
}

