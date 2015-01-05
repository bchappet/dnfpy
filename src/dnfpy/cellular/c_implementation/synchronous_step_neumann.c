#include <stdio.h>
#include "synchronous_step.h"
#define NB_NEUMANN 5
#define N 0
#define S 1
#define E 2
#define W 3
#define CELL 4

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
void synchronous_step_neumann(uchar *data,uchar *result,int m,int n,int depth,
                cell_comp_cb cell_computation,cell_args args){
        int i,j;
        uchar *data_neighs[NB_NEUMANN];/**The data should not be  modifiable**/
        uchar *result_neighs[NB_NEUMANN];/**The result are modifiable**/
        /**We first have to copy data in result**/
        copy_array_uchar(data,result,m*n*depth);
        /**TODO wrap**/
        for(i = 1 ; i < m-1 ; i++){
            for(j = 1 ; j < n-1 ; j++){
                /*Construct the neighbourhood*/
                data_neighs[N] = data + (i-1)*(n*depth)+(j)*depth;
                data_neighs[S] = data + (i+1)*(n*depth)+(j)*depth;
                data_neighs[E] = data + (i)*(n*depth)+(j+1)*depth;
                data_neighs[W] = data + (i)*(n*depth)+(j-1)*depth;
                data_neighs[CELL] = data + (i)*(n*depth)+(j)*depth;

                result_neighs[N] = result + (i-1)*(n*depth)+(j)*depth;
                result_neighs[S] = result + (i+1)*(n*depth)+(j)*depth;
                result_neighs[E] = result + (i)*(n*depth)+(j+1)*depth;
                result_neighs[W] = result + (i)*(n*depth)+(j-1)*depth;
                result_neighs[CELL] = result + (i)*(n*depth)+(j)*depth;
                /*Set the new value for cell*/
                cell_computation(result_neighs,data_neighs,args);
            }
        }
}
