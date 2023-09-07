import pandas as pd

data = pd.read_csv('./bok_call_rate_result_fillna_final.csv')
data['date'] = pd.to_datetime(data['date'])

df = data.copy()

df.insert(2, 'in_a_month', "")
df.insert(3, 'rate2', "")
df.insert(4, 'up_down', "")

# 해당 날짜로부터 30일 뒤의 날짜 정보가 담긴 컬럼 추가
import datetime
for idx in df.index:
    df.loc[idx, 'in_a_month'] = df.loc[idx, 'date'] + datetime.timedelta(days=30)
    # df.loc[idx, 'in_a_month'] = df.loc[idx, 'date'] + pd.DateOffset(months=1)
df['in_a_month'] = pd.to_datetime(df['in_a_month'])


# 한 달 뒤로 세팅된 날짜의 금리 정보 가져오기
for i in df.index:
    for j in df.index:
        if df.loc[i, 'in_a_month'] == df.loc[j, 'date']:
            df.loc[i, 'rate2'] = df.loc[j, 'rate']


# 한 달 후의 금리와 비교해서 '유지', '하락', '상승'으로 라벨링
for idx in df.index:
    if df.loc[idx, 'rate2'] != "":
        if df.loc[idx, 'rate'] == df.loc[idx, 'rate2']:
            df.loc[idx, 'up_down'] = '유지'
        
        elif df.loc[idx, 'rate'] > df.loc[idx, 'rate2']:
            df.loc[idx, 'up_down'] = '하락'

        elif df.loc[idx, 'rate'] < df.loc[idx, 'rate2']:
            df.loc[idx, 'up_down'] = '상승'

# 날짜 정보가 문자열로 저장된 date 컬럼 추가 
result_df = df.rename(columns={'date':'datetime'})
result_df.insert(1, 'date', "")

for idx in result_df.index:
    result_df.loc[idx, 'date'] = ''.join(str(result_df.loc[idx, 'datetime']).split('-'))[:8]

# 내보내기
result_df.to_csv('test.csv', index=False)