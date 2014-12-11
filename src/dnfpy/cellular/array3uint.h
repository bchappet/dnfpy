#ifndef ARRAY3UINT_H
#define ARRAY3UINT_H

typedef unsigned char uchar;


uchar **ptr_array3_uchar(int m, int n,int depth);
void free_ptr_array3_uchar(uchar **array);
void **copy_ptr_array3_uchar(uchar** source,uchar** dest);
void print_ptr_array3_uchar(uchar **array,int m, int n, int depth);

#endif
