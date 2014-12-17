#include "cellular_computation.h"
#include <assert.h>
#include <stdio.h>
#include "array_uchar.h"


void test_new(int size){
    cellular_array * ca;
    ca = new_cellular_array(size,size,1);
    print_ca(ca);
    delete_cellular_array(ca);
}

void test_update_cellular_array(int size){
    cellular_array * ca;
    ca = new_cellular_array(size,size,1);
    assert(ca->current == 0);
    update_cellular_array(ca);
    assert(ca->current == 1);
    update_cellular_array(ca);
    assert(ca->current == 0);
    delete_cellular_array(ca);
}

void test_update_life(int size){
    cellular_array * ca;
    uchar *data;
    ca = new_cellular_array(size,size,1);
    data = ca->buffers[ca->current];
    data[5*ca->n+5] = 1;
    data[5*ca->n+6] = 1;
    data[5*ca->n+7] = 1;
    data[6*ca->n+5] = 1;
    data[6*ca->n+6] = 1;
    data[6*ca->n+4] = 1;
    data[1*ca->n+1] = 1;

    print_ca(ca);
    update_cellular_array(ca);
    print_ca(ca);
    update_cellular_array(ca);
    print_ca(ca);
    
    delete_cellular_array(ca);
}


int main(void){
    test_new(100);
    printf("\n");
    test_update_cellular_array(10);
    test_update_life(10);
    return 0;
}

