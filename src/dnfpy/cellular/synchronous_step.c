#include "synchronous_step.h"
#define NB_MOORE 9

/**
 * Perform a cellular computation on data and return the result in result
 * data: previous state
 * result: next state
 * m: nb row
 * n: nb column
 * @precondition: 
 *  1) data is initialized
 *  2) result is initialized
 */
void synchronous_step(uchar *data,uchar *result,int m,int n,int depth,
                cell_comp_cb cell_computation){
        int i,j,a,b;
 uchar *data_neighs[NB_MOORE];/**The data are not modifiable**/
        int neigh_index;
        /**TODO wrap**/
        for(i = 1 ; i < m-1 ; i++){
            for(j = 1 ; j < n-1 ; j++){
                    /*Construct the neighbourhood*/
                    neigh_index = 0;
                    for(a=-1;a < 2;a++){
                        for(b=-1;b < 2;b++){
                            data_neighs[neigh_index] = data + (i+a)*(n*depth)+(j+b)*depth;
                            neigh_index ++;
                        }
                    }
                    /*Set the new value for cell*/
                    cell_computation(result +(i*n*depth+j*depth),data_neighs);
            }
        }
}
