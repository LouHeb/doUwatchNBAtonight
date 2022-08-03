

from basketball_reference_scraper.pbp import get_pbp


df = get_pbp('2022-06-16', 'GSW', 'BOS')


file = open("test.txt","w") 


for i in range (0,len(df['BOSTON_SCORE'])):
    file.write(str(df['QUARTER'][i])+' '+str(df['TIME_REMAINING'][i])+' '+str(df['GOLDEN STATE_SCORE'][i])+' '+str(df['BOSTON_SCORE'][i])+'\n')
file.close()
