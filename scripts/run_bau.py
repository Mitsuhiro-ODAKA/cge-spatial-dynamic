import os, json, pandas as pd
from pyomo.environ import SolverFactory
from models.cge_model import build_model
from models.parameters import param_data

def run_bau():
    # キャリブレーション結果読み込み
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..','models','calibrated_params.json'))
    with open(path) as f:
        d = json.load(f)
    param_data['alpha'] = d['alpha']
    param_data['X0']    = d['X0']

    # BAU: τ=0, g は parameters.py のデフォルトを使用
    param_data['tau'] = 0.0

    # モデル構築＆解く
    model = build_model(param_data)
    solver = SolverFactory('cbc')
    solver.solve(model)

    # 集計：GDP, emissions
    records = []
    for r in model.R:
        for t in model.T:
            outs = {s: model.X[r,s,t].value for s in model.S}
            gdp  = sum(outs.values())
            emis = sum(outs[s] * param_data['ef'][s] * (1 if t>0 else 0)
                       for s in model.S)
            records.append({'region':r, 'time':t, 'GDP':gdp, 'emissions':emis})

    df = pd.DataFrame(records)

    # CSV出力
    odir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..','outputs','tables'))
    os.makedirs(odir, exist_ok=True)
    csv = os.path.join(odir, 'results_bau.csv')
    df.to_csv(csv, index=False)
    print(f"BAU results → {csv}")

if __name__=='__main__':
    run_bau()
