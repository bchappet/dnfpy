#ifndef ARRAY3UINT_H
#define ARRAY3UINT_H

typedef unsigned char uchar;


/**
 *  Free the array and the data
 */
void deep_free_array_uchar(uchar **array,int size);
/**
 *  Free only the array, the data are not freed
 */
void shallow_free_array_uchar(uchar **array);
/**
 *  Copy pointers and data
 */
void deep_copy_array_uchar(uchar** source,uchar** dest,int size);
/**
 *Copy only pointers
 */
void shallow_copy_array_uchar(uchar** source,uchar** dest,int size);
/**
 *Print the array as a 3d array
 */
void print_array_uchar(uchar **array,int m, int n, int depth);
/*
 * Init the array to specified value
 * @precond: must be deeply allocated
 */
void init_array_uchar(uchar ** array,int size, uchar value);
/*
 *  Allocation of every pointer in the array
 */
void deep_allocation_array_uchar(uchar ** array,int size);
/**
 * Allocate an array of uchar*.
 */
uchar **shallow_allocation_array_uchar(int size);
#endif
