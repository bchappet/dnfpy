#ifndef CELLNSPIKE_H
#define CELLNSPIKE_H
#include <iostream>
#include "module.h"
class CellNSpike: public Module
{
public:
    CellNSpike(int row,int col);
    virtual void computeState() override;
    /**
     * @brief synch for computational speed we will not use register. So no synch needed
     */
    virtual void synch() override{}

    /**
    * @brief reset WARNING : does not reset "dead"
    */
    virtual void reset() override;

    virtual void getAttribute(int index,void* value) override{
        switch(index){
        case NB_BIT_RECEIVED:
            *((int*)value) = this->nbBitReceived;
            //std::cout << "val : "<< *((int*)value) << std::endl;
            return;
        case ACTIVATED:*((bool*)value) = this->activated;return;
        case DEAD:*((bool*)value) = this->dead;return;
        }
    }


    virtual void setAttribute(int index, void* value) override{
        switch(index){
        case NB_BIT_RECEIVED:this->nbBitReceived = *((int*)value);return;
        case ACTIVATED:this->activated = *((bool*)value);return;
        case DEAD:this->dead=*((bool*)value);return;
        }
    }
    /**
     * @brief The CellNSpike_Params enum, nb spike emmited on exitation and proba for every direction
     */
    enum CellNSpike_Params {NB_SPIKE,PROBA_N,PROBA_S,PROBA_E,PROBA_W};

    virtual void setDefaultParams(ParamsPtr params) override;

    enum CellNSpike_Attributes{NB_BIT_RECEIVED,ACTIVATED,DEAD};

    void setDead(bool isDead);

protected:
    void emmit(int nbSpike,int toDirection);
    void receive(int nbSpike,int toDirection);
    /**
     * @brief nbBitReceived nb bit received since last reset
     */
    int nbBitReceived;
    /**
     * @brief activated if true the cell will emmit NB_SPIKE spikes and will set this.activated at false
     */
    bool activated;
    /**
     * @brief dead if true, the cell will do nothing on spike reception
     */
    bool dead;
};

#endif // CELLNSPIKE_H
