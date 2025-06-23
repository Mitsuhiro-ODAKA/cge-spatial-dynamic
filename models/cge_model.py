from pyomo.environ import *

def build_model(params):
    model = ConcreteModel()

    # Sets
    model.R = Set(initialize=params['regions'])
    model.S = Set(initialize=params['sectors'])
    model.T = Set(initialize=params['time'])

    # Parameters: α, X0, τ, g, ef
    def alpha_init(m, r, s):
        return params['alpha'][r][s]
    model.alpha = Param(model.R, model.S, initialize=alpha_init, mutable=True)

    def X0_init(m, r, s):
        return params['X0'][r][s]
    model.X0 = Param(model.R, model.S, initialize=X0_init, mutable=False)

    model.tau = Param(initialize=params['tau'], mutable=True)
    model.g   = Param(initialize=params['g'],   mutable=True)

    model.ef  = Param(model.S, initialize=params['ef'], mutable=False)

    # Variables: 生産量
    model.X = Var(model.R, model.S, model.T, domain=NonNegativeReals)

    # 初期期を固定
    def init_rule(m, r, s):
        return m.X[r, s, 0] == m.X0[r, s]
    model.Init = Constraint(model.R, model.S, rule=init_rule)

    # 動的等式：外生成長＋炭素税
    def dyn_rule(m, r, s, t):
        if t == 0:
            return Constraint.Skip
        return m.X[r, s, t] == \
            (1 + m.g) * m.alpha[r, s] * sum(m.X[r, sp, t-1] for sp in m.S) \
            - m.tau * m.ef[s] * m.X[r, s, t-1]
    model.Dynamic = Constraint(model.R, model.S, model.T, rule=dyn_rule)

    return model
