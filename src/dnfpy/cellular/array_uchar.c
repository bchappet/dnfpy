/*Utility for array 3d unsigned char*/

#include<stdlib.h>
#include"array_uchar.h"
#include<stdio.h>



uchar *allocation_array_uchar(int size){
   uchar *array;
   array=(uchar *)malloc((size_t) (sizeof(uchar) * size));
   if (!array){
      printf("In *array_uchar. Allocation of memory for uchar array \
                      of size %d failed.",size);
      exit(0); 
    }
   return array;
}

/*
 * Init the array to specified value
 */
void init_array_uchar(uchar * array,int size, uchar value){
    int i;
    for(i = 0 ; i < size ; i++){
          array[i] = value;
    }
}



void print_array_uchar(uchar * array,int m, int n, int depth){
    int i,j,k;
    for(i = 0; i < m;i ++){
        for(j = 0; j < n;j ++){
            printf("[");
            for(k = 0; k < depth;k ++)
                printf("%d,",(array[i * n * depth + j*depth + k]));
            printf("],");
        }
        printf("\n");
    }

}

void free_array_uchar(uchar *array){
    free((uchar *)array);
}

void copy_array_uchar(uchar* source,uchar* dest,int size){
    int i;
    for(i = 0; i < size;i ++){
            dest[i] = source[i];
     }
}


/**
 * Return an array of uchar* initialized with value
 */
uchar* new_array_uchar(int size,uchar value){
    uchar* array;
    array = allocation_array_uchar(size);
    init_array_uchar(array,size,value);
    return array;
}
