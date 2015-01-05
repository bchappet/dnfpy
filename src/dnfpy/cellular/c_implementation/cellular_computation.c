#include <stdio.h>
#include "array_uchar.h"
#include "cellular_computation.h"
#include "synchronous_step.h"
#include <stdlib.h>



extern void compute_cell(uchar *newCell,uchar **neighs);




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
        ca->cell_computation = compute_cell;
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
    synchronous_step(ca->buffers[ca->current],ca->buffers[next],ca->n,ca->m,ca->depth,ca->cell_computation);
    ca->current = next;
}





void print_ca(cellular_array *ca){
    print_array_uchar(ca->buffers[ca->current],ca->m,ca->n,ca->depth);
    printf("\n");
}




