#include "array_uint.h"
#include <stdio.h>
#include <assert.h>
#include<stdlib.h>

void test_construction(int m,int n,int depth){
        int size;
        uchar **arr;

        size = m*n*depth;
        arr = shallow_allocation_array_uchar(size);
        assert(arr);
        deep_allocation_array_uchar(arr,size);
        assert(arr[m*n]);
        init_array_uchar(arr,size,255);
        assert(*arr[m*n]==255);
        deep_free_array_uchar(arr,size);
        shallow_free_array_uchar(arr);
        /**assert(!arr);**/
}

uchar **construct(int size,uchar value){
        uchar **arr;
        arr = shallow_allocation_array_uchar(size);
        deep_allocation_array_uchar(arr,size);
        init_array_uchar(arr,size,value);
        return arr;

}

void destruct(uchar ** arr, int size){
        deep_free_array_uchar(arr,size);
        shallow_free_array_uchar(arr);
}

void test_memory_load(int iteration,int size){
        int i;
        uchar ** arr;
        for(i = 0 ; i < iteration; i ++){
                arr = construct(size,255);
                destruct(arr,size);
        }
}

void test_shallow_copy(int size){
        uchar **arr;
        uchar **copy;
        uchar value;
        value = 102;
        arr = construct(size,1);
        init_array_uchar(arr,size,value);
        assert(*arr[size-1] == value);
        copy = shallow_allocation_array_uchar(size);
        shallow_copy_array_uchar(arr,copy,size);
        assert(*copy[size-1] == value);
        *arr[1] = 12;
        assert(*arr[1] == 12); 
        assert(*copy[1] == 12); 

        shallow_free_array_uchar(copy);
        deep_free_array_uchar(arr,size);
        shallow_free_array_uchar(arr);
}

void test_deep_copy(int size){
        uchar **arr;
        uchar **copy;
        uchar value;
        value = 102;
        arr = construct(size,1);
        init_array_uchar(arr,size,value);
        assert(*arr[size-1] == value);
        copy = shallow_allocation_array_uchar(size);
        deep_allocation_array_uchar(copy,size); 
        deep_copy_array_uchar(arr,copy,size);
        assert(*copy[size-1] == value);
        *arr[1] = 12;
        assert(*arr[1] == 12); 
        assert(*copy[1] != 12); 

        shallow_free_array_uchar(arr);
        deep_free_array_uchar(arr,size);
        shallow_free_array_uchar(copy);
        deep_free_array_uchar(copy,size);
}

void test_new_array_uchar(int size){
    uchar ** arr;
    arr = new_array_uchar(size,255);
    assert(*arr[size-1] == 255);
    free_array_uchar(arr,size);
}


int main(void){
        test_construction(10,10,3); 
        test_construction(1000,1000,3); 
        test_memory_load(1,10000000);
        test_shallow_copy(100);
        test_new_array_uchar(100);
        return 0;
}

