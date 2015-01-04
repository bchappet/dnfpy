#ifndef TEST_H
#define TEST_H


template <typename T>
T** newArray(int size){
    T ** array;

    array = new T*[size];
    for(int i = 0 ; i < size ; i++){
        array[i] = new T[size];
    }
    return array;
}

#endif // TEST_H
