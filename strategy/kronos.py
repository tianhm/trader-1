import sys
import os
import django
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.environ["DJANGO_SETTINGS_MODULE"] = "dashboard.settings"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from model import Kronos, KronosTokenizer, KronosPredictor
from panel.models import MainBar, to_df
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    tokenizer = KronosTokenizer.from_pretrained("D:/Github/Kronos/token_model/", local_files_only=True)
    model = Kronos.from_pretrained("D:/Github/Kronos/base_model/", local_files_only=True)
    predictor = KronosPredictor(model, tokenizer, device="cuda:0", max_context=512)
    qs = MainBar.objects.filter(product_code=product_code).order_by('-time')[:300]
    df = to_df(qs, parse_dates=['time'])

    # 统一列名与类型
    df.rename(columns={
        'time': 'timestamps',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'volume': 'volume',
        'open_interest': 'amount',
    }, inplace=True)

    use_cols = ['timestamps', 'open', 'high', 'low', 'close', 'volume']
    df = df[use_cols].copy()

    # 仅保留最后 need_rows 行用于后续切分（前250, 预测50）
    if len(df) < need_rows:
        raise RuntimeError(f"MainBar数据不足{need_rows}行，当前仅有{len(df)}行")
    df[['timestamps', 'open', 'high', 'low', 'close', 'volume', 'amount']].to_csv(csv_path, index=False)