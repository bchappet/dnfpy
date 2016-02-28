#ifndef SEQUENCECONNECTER_H
#define SEQUENCECONNECTER_H
#include "connecter.h"
/**
 * Connect the router to each other adding one neigbour for random bit propagation
 * it is a sequence connection:
 * 1 2 3 4 
 * 5 6 7 8
 * 9 ....12
 *
 * 12 linked to 1
 */
class SequenceConnecter:public Connecter
{
public:

    /**
     * 
     */
    virtual void connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray) const override;
    virtual void cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell)const ;


};

#endif // SEQUENCECONNECTER_H
