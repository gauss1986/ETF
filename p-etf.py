from pyomo.environ import *
import random

random.seed(1000)

model = AbstractModel()
# using the notations in A.H. Chen et al., Chap6 Handbook of portfolio construction 

# No. of risky assets
model.n = Param(within=PositiveIntegers)

# allow short position. Change to NonNegativeINtegers to only allow long position
model.I = RangeSet(1,model.n)
model.J = RangeSet(1,model.n)

model.rf = Param()
model.gamma = Param()
model.lam = Param()

model.x0 = Param(model.I, default=0)
model.rbar = Param(model.I)
model.cov = Param(model.I, model.I)
#model2.y0 = Param(initialize=1-sum(i for i in model2.x0))

# xb, xs, x and y
model.xb = Var(model.I, bounds=(0,1))
model.xs = Var(model.I, bounds=(0,0.2))
model.x = Var(model.I, bounds=(0,1))
model.y = Var(bounds=(0,1))

# objective
def cost_(model):
    return -model.rf*model.y - sum(model.rbar[i]*model.x[i] for i in model.I) \
            + model.gamma * sum(sum(model.cov[i,j]*model.x[j] for j in model.J)*model.x[i] for i in model.I)\
            - model.lam * (model.y + sum(model.x))
model.cost = Objective(rule=cost_)

# locate risky assets
#model.risky = ConstraintList()
#for i in range(N):
def risky_(model,i):
    model.x[i] == model.x0[i] + model.xb[i] - model.xs[i]
model.risky = Constraint(model.I,rule=risky_)
    
# capital constraint
def capital_(model):
    return model.y + sum(model.x[i] + cost(xb[i],rate) + cost(xs[i],rate) for i in model.I) <= 1 
model.capital = Constraint(rule=capital_)
