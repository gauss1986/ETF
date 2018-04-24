from __future__ import division
from pyomo.environ import *
import pandas as pd

def cost(x):
    """
    compute cost based on the piece-wise linear rate table
    """

    # define the piece-wise linear rate table
    rate = pd.DataFrame(index=range(5),columns=[['level','cost_ratio']])
    for i in range(5):
        rate.iloc[i] = [(i+1)/5., (5-i)**2/250.]

    n = 0    
    c = float(rate.loc[0,'cost_ratio']) * x
    while float(rate.loc[n,'level']) < value(x):
        c += (float(rate.loc[n+1,'cost_ratio'])-float(rate.loc[n,'cost_ratio'])) * (x-float(rate.loc[n,'level']))
        n += 1
        
    return c

model = AbstractModel()
# using the notations in A.H. Chen et al., Chap6 Handbook of portfolio construction 

# No. of risky assets
model.n = Param(within=PositiveIntegers)

# allow short position. Change to NonNegativeINtegers to only allow long position
model.I = Set()
model.J = Set()

model.rf = Param()
model.gamma = Param()
model.lam = Param()

model.x0 = Param(model.I, default=0)
model.rbar = Param(model.I)
model.cov = Param(model.I, model.I)
#model2.y0 = Param(initialize=1-sum(i for i in model2.x0))

# xb, xs, x and y
def zeros(model, i):
    return (0)
model.xb = Var(model.I, bounds=(0,1), initialize=zeros)
model.xs = Var(model.I, bounds=(0,0.2), initialize=zeros)
model.x = Var(model.I, bounds=(0,1))
model.y = Var(bounds=(0,1))

# objective
def cost_(model):
    return -model.rf*model.y - sum(model.rbar[i]*model.x[i] for i in model.I) \
            + model.gamma * sum(sum(model.cov[i,j]*model.x[j] for j in model.J)*model.x[i] for i in model.I)\
            - model.lam * (model.y + sum(model.x[i] for i in model.I))
model.cost = Objective(rule=cost_)

# locate risky assets
def risky_(model,i):
    return model.x[i] == model.x0[i] + model.xb[i] - model.xs[i]
model.risky = Constraint(model.I,rule=risky_)
    
# capital constraint
def capital_(model):
    return model.y + sum(model.x[i] + cost(model.xb[i]) + cost(model.xs[i]) for i in model.I) <= 1 
model.capital = Constraint(rule=capital_)
