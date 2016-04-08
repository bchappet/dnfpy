#ifndef TEST_UTILS_H
#define TEST_UTILS_H
#define PRECISION 1000000


template <typename T>
void print_2D_array(T* array,int width,int height);
template <typename T>
void print_3D_array(T* array,int width,int height,int third);

template <typename T>
T* construct_array(int width,int height);
template <typename T>
T* construct_array3d(int width,int height,int third);

template <typename T>
int sum_array(T* array,int length);

void assertAlmostEquals(float a,float b,float precision=PRECISION);

#endif
