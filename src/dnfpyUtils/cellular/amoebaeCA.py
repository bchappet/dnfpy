
import cv2
import numpy as np
from dnfpy.cellular.cellularMap import CellularMap



class AmoebaeCA(CellularMap):
    """

    diffusion : child the amibe will use the gradient to go to the source of diffusino
    obstacle : child 
    """
    def __init__(self,name,size,pa=0.0,m=4,**kwargs):
        super().__init__(name=name,size=size,pa=pa,m=m,**kwargs)

    def init(self,size):
        return np.zeros((size,size),dtype=np.uint8)




    def _compute(self,size,diffusion,obstacle,m,pa):
        """
        TODO the amibe is still going to the obstacle when pa != 0 ou pa != 1
        """

        #Move randomly or move to excited cell
    
        X = self._data
        x = X[1:-1,1:-1]

        random = (np.random.random((size,size)) < pa)
        #print(random)

        rand_dir = np.random.randint(0,8,(size,size)) #if rand, we'll move in dir \in {N,NE,E,...,NW}
        #O is no obstacle
        O = ~cv2.copyMakeBorder(obstacle.astype(np.uint8),1,1,1,1,cv2.BORDER_CONSTANT).astype(np.bool)

        #no obstacle for each direction
        oN = O[2:  ,1:-1 ] 
        oNE = O[2:  ,0:-2]
        oE = O[1:-1,0:-2 ]
        oSE = O[0:-2,0:-2]
        oS = O[0:-2,1:-1 ]
        oSW = O[0:-2,2:  ]
        oW = O[1:-1,2:   ]
        oNW = O[2:  ,2:  ]


        XR = X & random #this cells move randomly
        #cell move randomly to a direction if there is no ostacle
        c2N = XR & (rand_dir == 0) & oN
        c2NE = XR & (rand_dir == 1) & oNE
        c2E = XR & (rand_dir == 2) & oE
        c2SE = XR & (rand_dir == 3) & oSE
        c2S = XR & (rand_dir == 4) & oS
        c2SW = XR & (rand_dir == 5) & oSW
        c2W = XR & (rand_dir == 6) & oW
        c2NW = XR & (rand_dir == 7) & oNW





        #otherwise we go to one of excited cell


        D = cv2.copyMakeBorder(diffusion,1,1,1,1,cv2.BORDER_CONSTANT)
        d =diffusion
        dm1 = d-1
        A = (D > 0)[1:-1,1:-1]

        

        #The cell did not move randomly
        noMotion =  ~( c2N | c2NE | c2E | c2SE | c2S | c2SW | c2W |c2NW)

        #The cell follow gradient if it is on activation front
        XAR = X & A & noMotion


        #We move to excited cell if
        #There is a cell, the cell is  excited, and one neigh is a-1
        #TODO should choose randomly the activated neigh to go

        c2N_e =  XAR &  (D[2:  ,1:-1  ] == dm1)     
        no_e = ~c2N_e
        c2NE_e = XAR &  (D[2:  ,0:-2  ] == dm1)  & no_e
        no_e &= ~c2NE_e
        c2E_e =  XAR &  (D[1:-1,0:-2  ] == dm1)  & no_e
        no_e &= ~c2E_e
        c2SE_e = XAR &  (D[0:-2,0:-2  ]  == dm1) & no_e
        no_e &= ~c2SE_e
        c2S_e =  XAR &  (D[0:-2,1:-1  ]  == dm1) & no_e
        no_e &= ~c2S_e
        c2SW_e = XAR &  (D[0:-2,2:    ]  == dm1) & no_e  
        no_e &= ~c2SW_e
        c2W_e =  XAR &  (D[1:-1,2:    ] == dm1)  & no_e
        no_e &= ~c2W_e
        c2NW_e = XAR &  (D[2:  ,2:    ] == dm1)  & no_e
        no_e &= ~c2NW_e



        #assert(np.max(c2N_e+c2S_e+c2W_e+c2E_e) <= 1)
        static =( X & no_e & noMotion)



        x[...] =  (
          c2N[0:-2,1:-1] | c2NE[0:-2,2:] | c2E[1:-1,2: ] |c2SE[2: ,2: ] |c2S[2:  ,1:-1] |c2SW[2: ,0:-2] |  c2W[1:-1,0:-2] | c2NW[0:-2,0:-2]
          |c2N_e[0:-2,1:-1] | c2NE_e[0:-2,2:] | c2E_e[1:-1,2: ] |c2SE_e[2: ,2: ] |c2S_e[2:  ,1:-1] |c2SW_e[2: ,0:-2] |  c2W_e[1:-1,0:-2] | c2NW_e[0:-2,0:-2]

         | static[1:-1,1:-1]
       )


    def onClick(self,x,y):
        self._data[y,x] = 1
 
