#ifndef CELLULAR_COMPUTATION_H
#define  CELLULAR_COMPUTATION_H

#include "array_uchar.h"


struct CellularArray
{
    uchar **buffers;/*Array of arays*/
    int current;/*index of buffer holding current data**/
    int n;
    int m;
    int depth;
    int nb_buffer;
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

/**
 * Perform a cellular computation on data and return the result in result
 * @precondition: 
 *  1) data is initialized
 *  2) result is deeply allocated
 */
void synchronous_step(uchar *data,uchar *result,int m,int n,int depth);



void print_ca(cellular_array *ca);

#endif
