#include "mooreconnecter.h"

void MooreConnecter::cellConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir) const{
    if(neighCell!=nullptr){
        cell->addNeighbour(neighCell);
    }
}

void MooreConnecter::connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray,bool wrap) const{

    std::vector<Module::ModulePtr> inputs;
    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
           // std::cout << "i,j: (" << i << "," << j << ")" << std::endl;
            inputs.clear();
            int dir = 0;
            for(int a = -1 ; a <= 1 ; a++){
                for(int b = -1 ; b <= 1; b++){
                    Module::ModulePtr cell = cellArray[i][j];
                    if(a!=0 || b!= 0){
                       // std::cout << "(" << i+a << "," << j+b << ")" << std::endl;
                        if(this->within_border(i+a,j+b,height,width)){
                           // std::cout << "passed" << std::endl;
                            this->cellConnection(cell,cellArray[i+a][j+b],dir);
                        }else{
                            if(wrap)
                                this->cellConnection(cell,cellArray[(i+a)%height][(j+b)%width],dir);
                            else
                                this->cellConnection(cell,nullptr,dir);
                        }
                    }
                    dir ++;
                }
            }
        }
    }
}

