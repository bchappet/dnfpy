#include "cellnspike.h"
#include "neumannconnecter.h"

#include <stdlib.h>     /* srand, rand */
#include <iostream>

#define PRECISION_RAND 1000000

int applyProba(float proba, int n);
CellNSpike::CellNSpike(int row , int col): Module(row,col)
{


    //attribute
    this->nbBitReceived = 0;
    this->activated = false;
    this->dead = false;
}

void CellNSpike::reset(){
    Module::reset();
    this->nbBitReceived = 0;
    this->activated = false;
}

void CellNSpike::computeState(){
    if(this->activated && !this->dead){
        //emmit NB_SPIKE to the 4 neigbours
        for(int i = 0 ; i < 4; i++){
            this->emmit(this->getParam<int>(NB_SPIKE),i);
        }
        this->activated = false;

    }
}

void CellNSpike::setDefaultParams(ParamsPtr params){

    params->push_back(new int(20));//NB_SPIKE
    params->push_back(new float(1.0));//PROBA_N
    params->push_back(new float(1.0));//PROBA_S
    params->push_back(new float(1.0));//PROBA_E
    params->push_back(new float(1.0));//PROBA_W
    //std::cout << "inside NSpike : " << params->size() << std::endl;

}


void CellNSpike::emmit(int nbSpike,int toDirection){
    int nb_spike_to_send = 0;
    nb_spike_to_send = applyProba(this->getParam<float>(toDirection+1),nbSpike);//proba corespond to direction of target
    if(nb_spike_to_send > 0){
       ((CellNSpike*)this->neighbours[toDirection].get())->receive(nb_spike_to_send,toDirection);
    }

}
/**
 * @brief CellNSpike::receive this position compared to the cell whi sent the spikes N (0) S(1) E(2) W(3)
 * @param nbSpike
 * @param fromDirection
 */
void CellNSpike::receive(int nbSpike, int toDirection){
    this->nbBitReceived += nbSpike;
    if(!this->dead){
        switch(toDirection){
        case NeumannConnecter::N:
            emmit(nbSpike,NeumannConnecter::N);
            emmit(nbSpike,NeumannConnecter::E);
            emmit(nbSpike,NeumannConnecter::W);
            return;
        case NeumannConnecter::S:
            emmit(nbSpike,NeumannConnecter::S);
            emmit(nbSpike,NeumannConnecter::E);
            emmit(nbSpike,NeumannConnecter::W);
            return;
        case NeumannConnecter::E:
            emmit(nbSpike,NeumannConnecter::E);
            return;
        case NeumannConnecter::W:
            emmit(nbSpike,NeumannConnecter::W);
            return;
        }
    }

}

void CellNSpike::setDead(bool isDead){
    this->dead = isDead;
}

int applyProba(float proba,int n){
    int sum = 0;
    int probaInt = (proba * PRECISION_RAND);
    for(int i = 0 ; i < n ; i++){
        sum += (rand() % PRECISION_RAND <= probaInt);
    }
    return sum;
}
