#include "sequenceConnecter.h"

/**
 * To avoid interpath correlation we connect differently for odd and even row and col
 */
void SequenceConnecter::cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const{
    int row = cell->getRow();
    int col = cell->getCol();
    if(neighCell != nullptr){
        switch(dir){
        case N:
            if( col % 2 == 0) 
                cell->getSubModule(E).get()->addNeighbour(neighCell.get()->getSubModule(E));
            else
                cell->getSubModule(W).get()->addNeighbour(neighCell.get()->getSubModule(W));
            break;
        case S:
            if (col % 2 == 0)
                cell->getSubModule(W).get()->addNeighbour(neighCell.get()->getSubModule(W));
            else
                cell->getSubModule(E).get()->addNeighbour(neighCell.get()->getSubModule(E));
            break;
        case E:
            if( row % 2 == 0)
                cell->getSubModule(S).get()->addNeighbour(neighCell.get()->getSubModule(S));
            else
                cell->getSubModule(N).get()->addNeighbour(neighCell.get()->getSubModule(N));
            break;
        case W:
            if(row % 2 == 0)
                cell->getSubModule(N).get()->addNeighbour(neighCell.get()->getSubModule(N));
            else
                cell->getSubModule(S).get()->addNeighbour(neighCell.get()->getSubModule(S));
            break;
        }
    }
}

/**wrap x-1 **/
int wrapDown(int x,int dim){
    int wrappedX;
    if(dim % 2 == 1){ //odd dimension isthe difficult case
        if(x == 0)
            wrappedX = dim-1; 
        else if(x == 1)
            wrappedX = dim-2;
        else
            wrappedX = (x-2 + dim) % dim;

    }else{
        wrappedX = (x-2 + dim) % dim;
    }
    return wrappedX;
}

/**wrap x+1 **/
int wrapUp(int x,int dim){
    int wrappedX;
    if(dim % 2 == 1){ //odd dimension isthe difficult case
        if(x == dim - 1)
            wrappedX = 0; 
        else if(x == dim - 2)
            wrappedX = 1;
        else
            wrappedX = (x+2 ) % dim;

    }else{
        wrappedX = (x+2 ) % dim;
    }
    return wrappedX;
}
/**For the sequence connecter the wrapping is shifted to avoid redondancy**/
void SequenceConnecter::connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray,bool wrap) const{


    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
            Module::ModulePtr cell = cellArray[i][j];
            this->cellConnection(cell);
            if(this->within_border(i-1,j,height,width))
                this->cellNeighbourConnection(cell,cellArray[i-1][j],N);
            else{
                if(wrap)
                    this->cellNeighbourConnection(cell,cellArray[(i-1 + height)%height][wrapUp(j,width)],N);
                else
                    this->cellNeighbourConnection(cell,nullptr,N);
            }

            if(this->within_border(i+1,j,height,width))
                this->cellNeighbourConnection(cell,cellArray[i+1][j],S);
            else{
                if(wrap)
                    this->cellNeighbourConnection(cell,cellArray[(i+1)%height][wrapDown(j,width)],S);
                else
                    this->cellNeighbourConnection(cell,nullptr,S);
            }
                

            if(this->within_border(i,j+1,height,width))
                this->cellNeighbourConnection(cell,cellArray[i][j+1],E);
            else{
                if(wrap)
                    this->cellNeighbourConnection(cell,cellArray[wrapDown(i,height)][(j+1)%width],E);
                else
                    this->cellNeighbourConnection(cell,nullptr,E);
            }

            if(this->within_border(i,j-1,height,width))
                this->cellNeighbourConnection(cell,cellArray[i][j-1],W);
            else{
                if(wrap)
                    this->cellNeighbourConnection(cell,cellArray[wrapUp(i,height)][(j-1 + width)%width],W);
                else
                    this->cellNeighbourConnection(cell,nullptr,W);
            }


        }
    }
}

/**For the sequence connecter short the wrapping is not shifted**/
void SequenceConnecterShort::connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray,bool wrap) const{


    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
            Module::ModulePtr cell = cellArray[i][j];
            this->cellConnection(cell);
            if(this->within_border(i-1,j,height,width))
                this->cellNeighbourConnection(cell,cellArray[i-1][j],N);
            else{
                if(wrap)
                    this->cellNeighbourConnection(cell,cellArray[(i-1 + height)%height][j],N);
                else
                    this->cellNeighbourConnection(cell,nullptr,N);
            }

            if(this->within_border(i+1,j,height,width))
                this->cellNeighbourConnection(cell,cellArray[i+1][j],S);
            else{
                if(wrap)
                    this->cellNeighbourConnection(cell,cellArray[(i+1)%height][j],S);
                else
                    this->cellNeighbourConnection(cell,nullptr,S);
            }
                

            if(this->within_border(i,j+1,height,width))
                this->cellNeighbourConnection(cell,cellArray[i][j+1],E);
            else{
                if(wrap)
                    this->cellNeighbourConnection(cell,cellArray[i][(j+1)%width],E);
                else
                    this->cellNeighbourConnection(cell,nullptr,E);
            }

            if(this->within_border(i,j-1,height,width))
                this->cellNeighbourConnection(cell,cellArray[i][j-1],W);
            else{
                if(wrap)
                    this->cellNeighbourConnection(cell,cellArray[i][(j-1 + width)%width],W);
                else
                    this->cellNeighbourConnection(cell,nullptr,W);
            }


        }
    }
}



