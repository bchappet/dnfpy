#include <Python.h>
#include "numpy/arrayobject.h"
#include <stdio.h>
#define NB_VON_NEUMANN 5
#define NB_MOORE 9
#define CELL 0
#define N 1
#define S 2
#define E 3
#define W 4
#define NE 5
#define SE 6
#define NW 7
#define SW 8


void printArray(double **v,int m,int n);
double **ptrArray(int m,int n);
void free_ptrArray(double **v);
void compute(double* pvois[],double vois[]);
void copyNpArray2CArray(PyArrayObject * array,double **copy);
void copyCArray2NpArray(double **array,PyArrayObject * copy);


void computeSum(double* pvois[NB_VON_NEUMANN],double vois[NB_VON_NEUMANN]){
    double sum ;
    sum = vois[N] + vois[S] + vois[E] + vois[W];
    *pvois[CELL] = sum;
}
void computeConway(double* pvois[NB_MOORE],double vois[NB_MOORE]){
    double sum ;
    sum = vois[N] + vois[S] + vois[E] + vois[W] + 
            vois[NE] + vois[SE] + vois[NW] + vois[SW];
    if(vois[CELL] == 0.){ //cell is dead
         if(sum > 2.9 && sum < 3.1 )
             *pvois[CELL] = 1.0;
         else
             *pvois[CELL] = 0.0;

    }else{ //cell is alive
        if(sum < 1.9 || sum > 3.1)
             *pvois[CELL] = 0.0;
         else
             *pvois[CELL] = 1.0;
        
    }

}


static PyObject *cmod_syncUpdate(PyObject *self,PyObject *args)
{
        PyArrayObject *array;
        int i,j,cols,rows;
        double **copy; //c copy of the array
        char *data;//data of numpy array
        int stride_i,stride_j;//stride of data array
        double *pvois[NB_MOORE];
        double vois[NB_MOORE];
        

        if (!PyArg_ParseTuple(args, "O!",&PyArray_Type, &array)){
                return NULL;
        }

        if (array->nd != 2 || array->descr->type_num != PyArray_DOUBLE) {
                PyErr_SetString(PyExc_ValueError,"array must be two-dimensional and of type double");
                return NULL;
        }
        rows = array->dimensions[0];
        cols = array->dimensions[1];
        copy = ptrArray(rows,cols);
        copyNpArray2CArray(array,copy);

        data = array->data;
        stride_i = array->strides[0];
        stride_j = array->strides[1]; 
        
        //TODO wrap
        for(i = 1 ; i < rows-1 ; i++){
            for(j = 1 ; j < cols-1 ; j++){
                //Pointer on modifiable data
                pvois[CELL] = (double*)( copy + (i*cols+j));//C
                pvois[N] = (double*)( copy + ((i-1)*cols+j));//N
                pvois[S] = (double*)( copy + ((i+1)*cols+j));//S
                pvois[E] = (double*)( copy + (i*cols+(j+1)));//E
                pvois[W] = (double*)( copy + (i*cols+(j-1)));//W
                pvois[NE] = (double*)( copy + ((i-1)*cols+(j+1)));
                pvois[NW] = (double*)( copy + ((i-1)*cols+(j-1)));
                pvois[SE] = (double*)( copy + ((i+1)*cols+(j+1)));
                pvois[SW] = (double*)( copy + ((i+1)*cols+(j-1)));

                vois[CELL] = *(double*)( data + (i*stride_i+j*stride_j));//C
                vois[N] = *(double*)( data + ((i*stride_i-stride_i)+j*stride_j));//N
                vois[S] = *(double*)( data + ((i*stride_i+stride_i)+j*stride_j));//S
                vois[E] = *(double*)( data + (i*stride_i+(j*stride_j+stride_j)));//E
                vois[W] = *(double*)( data + (i*stride_i+(j*stride_j-stride_j)));//W
                vois[NE] = *(double*)( data + ((i*stride_i-stride_i)+j*stride_j+stride_j));
                vois[NW] = *(double*)( data + ((i*stride_i-stride_i)+j*stride_j-stride_j));
                vois[SE] = *(double*)( data + ((i*stride_i+stride_i)+j*stride_j+stride_j));
                vois[SW] = *(double*)( data + ((i*stride_i+stride_i)+j*stride_j-stride_j));

                computeConway(pvois,vois);
                
            }
        }

        copyCArray2NpArray(copy,array);
        free_ptrArray(copy);
        Py_RETURN_NONE;
}

void copyCArray2NpArray(double **array,PyArrayObject * copy){
        int i,j,cols,rows;
        double  value;//value of array at i,j
        char *data;//data of numpy array

        rows = copy->dimensions[0];
        cols = copy->dimensions[1];
        data = copy->data;
       
        for(i = 0 ; i < rows ; i++){
            for(j = 0 ; j < cols ; j++){
                    value = *((double *)(array + (i*cols+j)));
                    *(double*)(data + i * copy->strides[0] +
                                   j * copy->strides[1]) = value; 
            }
        }

}



void copyNpArray2CArray(PyArrayObject * array,double **copy){
        int i,j,cols,rows;
        double  value;//value of array at i,j
        char *data;//data of numpy array

        rows = array->dimensions[0];
        cols = array->dimensions[1];
        data = array->data;
       
        for(i = 0 ; i < rows ; i++){
            for(j = 0 ; j < cols ; j++){
                    value = *(double*)(data + i * array->strides[0] +
                                   j * array->strides[1]); 
                    *((double *)(copy + (i*cols+j))) = value;
            }
        }


}

void printArray(double **v,int m,int n){
    int i,j;
    for(i = 0; i < m;i ++){
        for(j = 0; j < n;j ++){
            printf("%f,",*((double*)(v + (i * n + j))));
        }
        printf("\n");
    }

}

/**
Allocate a contigous int array with m row and n column
return pointer to this array
**/
double **ptrArray(int m,int n) { 
   double **v;
   v=(double **)malloc((size_t) (m*n*sizeof(double)));
   if (!v){
      printf("In **ptrArray. Allocation of memory for int array failed.");
      exit(0); 
    }
   return v;
}

/**
Free the memory of a c array
**/
void free_ptrArray(double **v){
    free((double *)v);
}





static PyObject *cmod_trace(PyObject *self, PyObject *args)
{
        PyArrayObject *array;
        double sum,val;
        int i, n;

        if (!PyArg_ParseTuple(args, "O!",&PyArray_Type, &array)){
                return NULL;
        }

        if (array->nd != 2 || array->descr->type_num != PyArray_DOUBLE) {
                PyErr_SetString(PyExc_ValueError,"array must be two-dimensional and of type float");
                return NULL;
        }


        n = array->dimensions[0];
        if (n > array->dimensions[1])
                n = array->dimensions[1];
        sum = 0.;
        for (i = 0; i < n; i++){
                val =  *(double *)(array->data + i*array->strides[0] +
                                i*array->strides[1]);
                sum +=  val;
                      
        }


        return PyFloat_FromDouble(sum);


}

static PyMethodDef cmod_methods[] = {
           {"trace", cmod_trace, METH_VARARGS, NULL },
           {"syncUpdate",cmod_syncUpdate,METH_VARARGS,NULL},
           { NULL, NULL, 0, NULL }
};


void initcmod(void)
{
    Py_InitModule3("cmod", cmod_methods,"Extension numpy module example!");
    import_array();
}
