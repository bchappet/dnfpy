#include <stdio.h>
#include "array_uchar.h"
#include "cellular_computation.h"
#include <stdlib.h>
#define NB_MOORE 9
#define CELL 4
#define N 1
#define S 7
#define E 5
#define W 3
#define NE 2
#define SE 8
#define NW 0
#define SW 6


void compute_cell(uchar *newCell,uchar **neighs);

/**
 * Cell computation the new state will be set in newCell
 * We access the cell and neighbours previous state in neighs 
 */
void compute_cell(uchar *newCell,uchar **neighs){
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


/**
 * Construct a cellular array with m rows and n colums
 */
cellular_array *new_cellular_array(int m,int n,int depth){
        cellular_array * ca;
        uchar **buffers;
        int nb_buffer;
        int i;
        nb_buffer = 2;

        ca = (cellular_array*) malloc(sizeof(cellular_array));
        buffers = (uchar**) malloc(nb_buffer*sizeof(uchar*));
        for(i = 0 ;i < nb_buffer ;i++){
            buffers[i] = new_array_uchar(m*n*depth,0);
        }
        ca->buffers = buffers;
        ca->current = 0;
        ca->n = n;
        ca->m = m;
        ca->depth = depth;
        ca->nb_buffer = nb_buffer;
        return ca;
}


/**
 *Free the memory used by the cellular_array
 */
void delete_cellular_array(cellular_array *ca){
        int i;
        for(i = 0 ; i < ca->nb_buffer ; i++){
            free_array_uchar(ca->buffers[i]);
        }
        free(ca->buffers);
        free(ca);
}


/**
 *Perform the synchronous update on the cellular array
 */
void update_cellular_array(cellular_array *ca){
    int next;
    next = (ca->current + 1) % ca->nb_buffer;
    synchronous_step(ca->buffers[ca->current],ca->buffers[next],ca->n,ca->m,ca->depth);
    ca->current = next;
}



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
void synchronous_step(uchar *data,uchar *result,int m,int n,int depth){
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
                    compute_cell(result +(i*n*depth+j*depth),data_neighs);
            }
        }
}

void print_ca(cellular_array *ca){
    print_array_uchar(ca->buffers[ca->current],ca->m,ca->n,ca->depth);
    printf("\n");
}




