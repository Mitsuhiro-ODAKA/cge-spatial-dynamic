# models/parameters.py

param_data = {
    # モデル構造
    'regions': ['A', 'B', 'C'],
    'sectors': ['agriculture', 'manufacturing', 'services'],
    'time':    list(range(0, 11)),   # 0～10年

    # キャリブレーションで上書き
    'alpha': {},   # 生産シェア
    'X0':    {},   # 初期出力

    # 政策パラメータ
    'tau': 0.0,    # 炭素税率（BAU=0, Policy>0）

    # 外生的生産性成長率
    'g': 0.02,     # 例：2%/年

    # セクター別排出係数
    'ef': {
        'agriculture': 0.2,
        'manufacturing': 0.5,
        'services': 0.3
    }
}
