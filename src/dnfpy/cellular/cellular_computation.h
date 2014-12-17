#ifndef CELLULAR_COMPUTATION_H
#define  CELLULAR_COMPUTATION_H

#include "array_uchar.h"

typedef void (*cell_comp_cb)(uchar *newCell,uchar **neighs);

struct CellularArray
{
    uchar **buffers;/*Array of arays*/
    int current;/*index of buffer holding current data**/
    int n;
    int m;
    int depth;
    int nb_buffer;
    cell_comp_cb cell_computation;
    
};
typedef struct CellularArray cellular_array;



/**
 * Construct a cellular array with m rows and n colums
 */
cellular_array* new_cellular_array(int m,int n,int depth);

/**
 *Free the memory used by the cellular_array
 */
void delete_cellular_array(cellular_array *ca);

/**
 *Perform the synchronous update on the cellular array
 */
void update_cellular_array(cellular_array *ca);



void print_ca(cellular_array *ca);

#endif
