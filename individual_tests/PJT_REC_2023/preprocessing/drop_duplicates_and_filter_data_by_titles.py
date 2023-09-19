import pandas as pd

df = pd.read_csv('./naver_economy.csv')

# 본문 기준 중복 제거, 제목 기준 중복 제거
df.drop_duplicates('content', inplace=True)
df.drop_duplicates('title', inplace=True)

# 본문이 null인 행 제거, 제목이 null인 행 제거
df.dropna(axis=0, subset=['title'])
df.dropna(axis=0, subset=['content'])

# 본문의 글자수가 50자 이하인 행 제거
df = df[df['content'].apply(lambda x: len(str(x))>50)]

# 해당 텍스트가 포함된 행 제거
word_list = ['부고', '단신']
text = '|'.join(word_list)
df[~df['title'].str.contains(text)]

df.to_csv('./naver_economy_filtered.csv', index=None)