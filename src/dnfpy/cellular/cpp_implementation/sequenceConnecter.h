#ifndef SEQUENCECONNECTER_H
#define SEQUENCECONNECTER_H
#include "neumannconnecter.h"
/**
 * Opposite connection to RSDNF to avoid any correlation with spike propagation
 * 12 linked to 1
 * Cycle 2 (the period of propagation is res*res)
 */
class SequenceConnecter:public NeumannConnecter
{
public:

    virtual void cellConnection(Module::ModulePtr cell)const override {};
    virtual void cellNeighbourConnection(Module::ModulePtr cell,Module::ModulePtr neighCell,int dir)const override;
    virtual void connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray,bool wrap = false) const override;


};


/**
 * The connection are wrapped naturally
 * Cycle 1 (the period of propagation is res)
 */
class SequenceConnecterShort: public SequenceConnecter
{
public:

    virtual void connect(int width,int height,std::vector<std::vector<Module::ModulePtr>> &cellArray,bool wrap = false) const override;
};

#endif // SEQUENCECONNECTER_H
