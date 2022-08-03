



df = get_pbp('2022-06-16', 'GSW', 'BOS')


for i in range (0,len(df['BOSTON_SCORE'])):
    print(df['QUARTER'][i],df['TIME_REMAINING'][i],df['GOLDEN STATE_SCORE'][i],df['BOSTON_SCORE'][i])
