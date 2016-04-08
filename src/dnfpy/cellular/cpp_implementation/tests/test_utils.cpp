#include <iostream>
#include <assert.h>
#include "test_utils.h"


using namespace std;

template <typename T>
void print_2D_array(T* array,int width,int height){
    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
            cout << array[i*width + j] << ",";
        }
        cout << endl;
    }
}

template <typename T>
void print_3D_array(T* array,int width,int height,int third){
    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
            cout << "(";
            for(int k = 0 ; k < third ; k++){
                cout << array[i*(width*third) + j*third +k] << ",";
            }
            cout << ")," ;
        }
        cout << endl;
    }
}
template <typename T>
T* construct_array(int width,int height){
    T * array;
    array = new T[height*width];
    return array;
}

template <typename T>
T* construct_array3d(int width,int height,int third){
    T * array;
    array = new T[height*width*third];
    return array;
}

void assertAlmostEquals(float a,float b,float precision){
    assert(a-b <= 1./precision);
}

template <typename T>
int sum_array(T* array,int length){
    int sum = 0;
    for(int i = 0 ; i < length ; i++){
        sum = sum + array[i];
    }
    return sum;
}

template void print_2D_array<bool>(bool* array,int width,int height);
template bool* construct_array<bool>(int width,int height);
template int sum_array<bool>(bool* array,int length);
template void print_2D_array<int>(int* array,int width,int height);
template int* construct_array<int>(int width,int height);
template int sum_array<int>(int* array,int length);
template void print_3D_array<int>(int* array,int width,int height,int third);
template int* construct_array3d<int>(int width,int height,int third);
