#include "cell_computation.h"
/**
 * Cell computation the new state will be set in newCell game of life
 * We access the cell and neighbours previous state in neighs 
 */
void compute_cell_gol(uchar *newCell,uchar **neighs){
    uchar sum;
    uchar cell;
    sum = neighs[N][0] + neighs[S][0] + neighs[E][0] + neighs[W][0] + \
          neighs[NE][0] + neighs[NW][0] + neighs[SE][0] + neighs[SW][0];
    cell = neighs[CELL][0];
    if(cell == 0){
        if(sum == 3) *newCell =  1;
        else *newCell = 0;
    }else{
        if(sum < 2 || sum > 3){
                *newCell = 0;
        }else{
                *newCell = 1;
        }
    }
}



