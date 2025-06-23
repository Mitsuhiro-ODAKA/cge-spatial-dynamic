# scripts/calibrate.py

import os, json
import pandas as pd
from models.parameters import param_data

def calibrate():
    sam = pd.read_csv('../data/sam/sam_base.csv')
    sam['output'] = sam[['household','government','investment','export']].sum(axis=1)

    # ネスト辞書 α と初期出力 X0
    nested_alpha = {r: {} for r in param_data['regions']}
    nested_X0    = {r: {} for r in param_data['regions']}
    for r in param_data['regions']:
        df_r = sam[sam['region']==r]
        total = df_r['output'].sum()
        for s in param_data['sectors']:
            o = float(df_r[df_r['sector']==s]['output'].iloc[0])
            nested_alpha[r][s] = o / total
            nested_X0[r][s]    = o

    out = {
        'alpha': nested_alpha,
        'X0':    nested_X0
    }
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..','models','calibrated_params.json'))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"Calibration saved → {out_path}")

if __name__=='__main__':
    calibrate()
