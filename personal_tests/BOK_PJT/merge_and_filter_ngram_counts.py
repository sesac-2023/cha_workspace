import pandas as pd

# 파일 병합하고 상승, 하락별 카운트 누적합하기

merged_df_up = pd.DataFrame(columns=["ngram", "up_count"])
merged_df_down = pd.DataFrame(columns=["ngram", "down_count"])

file_names_up = [f"./counting_{i}_상승.csv" for i in range(7)]
file_names_down = [f"./counting_{i}_하락.csv" for i in range(7)]  

def merge_and_accumulate(file_names, merged_df, column_name):
    for file_name in file_names:
        df = pd.read_csv(file_name,skiprows=[0], names=["ngram", column_name] )
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    merged_df = merged_df.groupby('ngram')[column_name].sum().reset_index().sort_values(by=column_name, ascending=False, ignore_index=True)
    return merged_df

merged_df_up = merge_and_accumulate(file_names_up, merged_df_up, 'up_count')
merged_df_down = merge_and_accumulate(file_names_down, merged_df_down, 'down_count')

merged_df_up.to_csv('./ngram_counts_up.csv', index=False)
merged_df_down.to_csv('./ngram_counts_down.csv', index=False)

#==============================================================================#

# 상승, 하락 파일 최종 병합하고 min_count 15 적용하기

df1 = pd.read_csv('./ngram_count_up.csv')
df2 = pd.read_csv('./ngram_count_down.csv')

# 데이터프레임 병합하고 null값은 int 타입 0으로 채우기 (상승: 44003774행 / 하락: 75447825행)
merged_df = df1.merge(df2, on='ngram', how='outer')
merged_df['up_count'] = merged_df['up_count'].fillna(0).astype(int)
merged_df['down_count'] = merged_df['down_count'].fillna(0).astype(int)
merged_df['sum_count'] = merged_df['up_count'] + merged_df['down_count']
# merged_df.to_csv('./ngram_counts_not_filtered.csv', index=False)

# sum_count 컬럼 생성하고 상승, 하락 총 합계가 15미만인 행 삭제 (삭제 전: 75447825행 / 삭제 후: 1009828행)
merged_df['sum_count'] = merged_df['up_count'] + merged_df['down_count']
filtered_df = merged_df[merged_df['sum_count'] >= 15][['ngram', 'up_count', 'down_count']]

# 파일 내보내기
filtered_df.to_csv('./ngram_counts_merged_and_filtered.csv', index=False)