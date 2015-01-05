#ifndef SYNCHRONOUS_STEP_H
#define SYNCHRONOUS_STEP_H

#include "array_uchar.h"
struct CellArgs{
    
};
typedef struct CellArgs cell_args;
typedef void (*cell_comp_cb)(uchar **newCell,uchar **neighs,cell_args);


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
                cell_comp_cb cell_computation,cell_args args);
 

#endif
