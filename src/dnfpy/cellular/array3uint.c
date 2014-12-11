/*Utility for array 3d unsigned char*/


#include<stdlib.h>
#include"array3uint.h"
#include<stdio.h>




uchar **ptr_array3_uchar(int m, int n,int depth){
   uchar **array;
   array=(uchar **)malloc((size_t) (m*n*depth*sizeof(uchar)));
   if (!array){
      printf("In **ptr_array3_uchar. Allocation of memory for uchar array \
                      of size %d failed.",m*n*depth);
      exit(0); 
    }
   return array;;
}



void print_ptr_array3_uchar(uchar ** array,int m, int n, int depth){
    int i,j,k;
    for(i = 0; i < m;i ++){
        for(j = 0; j < n;j ++){
            printf("[");
            for(k = 0; k < depth;k ++)
                printf("%d,",*((uchar*)(array + (i * n * depth + j*depth + k))));
            printf("],");
        }
        printf("\n");
    }

}
