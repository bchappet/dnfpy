#include "cellular_computation.h"
#define NB_RECEIVED 0
#define TN 1
#define TS 2
#define TE 3
#define TW 4
#define N 0
#define S 1
#define E 2
#define W 3
#define CELL 4

/**
 *The depth should be 4 (1 for each transmiter
 */
void compute_cell_transmitters(uchar **newNeighs,uchar **neighs){
    if(neighs[CELL][TN] > 0){
        newNeighs[N][TN] += 1;
        newNeighs[N][TE] += 1;
        newNeighs[N][TW] += 1;

        newNeighs[N][NB_RECEIVED] += 1;

        newNeighs[CELL][TN] -= 1;
    }
    if(neighs[CELL][TS] > 0){
        newNeighs[S][TS] += 1;
        newNeighs[S][TE] += 1;
        newNeighs[S][TW] += 1;

        newNeighs[S][NB_RECEIVED] += 1;

        newNeighs[CELL][TS] -= 1;
    }
    if(neighs[CELL][TE] > 0){
        newNeighs[E][TE] += 1;
        newNeighs[E][NB_RECEIVED] += 1;
        newNeighs[CELL][TE] -= 1;
    }
    if(neighs[CELL][TW] > 0){
        newNeighs[W][TW] += 1;
        newNeighs[W][NB_RECEIVED] += 1;
        newNeighs[CELL][TW] -= 1;
    }



}
