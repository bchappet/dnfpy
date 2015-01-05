#ifndef ARRAY3UINT_H
#define ARRAY3UINT_H

typedef unsigned char uchar;

/**
 *Copy only pointers
 */
void copy_array_uchar(uchar* source,uchar* dest,int size);
/**
 *Print the array as a 3d array
 */
void print_array_uchar(uchar *array,int m, int n, int depth);
/*
 * Init the array to specified value
 * @precond: must be deeply allocated
 */
void init_array_uchar(uchar * array,int size, uchar value);
/*
 *  Allocation of every pointer in the array
 */
uchar * allocation_array_uchar(int size);

/**
 * Return an array of uchar* initialized with value
 */
uchar* new_array_uchar(int size,uchar value);

/**
 * completly free an array (check if deep freing is necessary) 
*/
void free_array_uchar(uchar *arr);
#endif
