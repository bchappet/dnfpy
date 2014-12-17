#define NB_MOORE 9
#define CELL 4
#define N 1
#define S 7
#define E 5
#define W 3
#define NE 2
#define SE 8
#define NW 0
#define SW 6
typedef unsigned char uchar;

/**
 * Interface for cell computation
 */
void compute_cell(uchar **newNeighs,uchar **neighs);
