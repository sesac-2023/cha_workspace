import pandas as pd

df = pd.read_csv('./naver_venture.csv', usecols=['url', 'comment'])
df = df.dropna()
df['comment'] = df['comment'].map(lambda x : eval(x))
df = df.explode('comment')

df['user_id'] = df['comment'].apply(lambda x : x['userIdNo'])
df['user_name'] = df['comment'].apply(lambda x : x['userName'])
df['date_upload'] = df['comment'].apply(lambda x : x['regTime'])
df['date_upload'] = [date__[:-5].replace('T', ' ') for date__ in df['date_upload']]
df['date_fix'] = df['date_upload']
df['good_cnt'] = df['comment'].apply(lambda x : x['sympathyCount'])
df['bad_cnt'] = df['comment'].apply(lambda x : x['antipathyCount'])
df['comment'] = df['comment'].apply(lambda x : x['contents'])
df['comment'] = df['comment'].apply(lambda x : x.replace('\x00', ''))
df.dropna(inplace=True)

df.to_csv('./naver_venture_comment.csv', index=None, escapechar='')