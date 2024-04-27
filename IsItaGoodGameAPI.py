#---
#       IMPORT LIBRARIES
#---

import numpy as np
from datetime import datetime, timedelta
#from basketball_reference_scraper.seasons import get_schedule
#from basketball_reference_scraper.pbp import get_pbp
import pandas as pd
from requests import get
from bs4 import BeautifulSoup


#---
#       DICTIONNARIES
#---

Lit_Day = {"01":"1st","02":"2nd","03":"3rd","04":"4th","05":"5th","06":"6th","07":"7th","08":"8th","09":"9th","10":"10th","11":"11th","12":"12th","13":"13th","14":"14th","15":"15th","16":"16th","17":"17th","18":"18th","19":"19th","20":"20th","21":"21st","22":"22nd","23":"23rd","24":"24th","25":"25th","26":"26th","27":"27th","28":"28th","29":"29th","30":"30th","31":"31st"}
Lit_Month = {'01':"January",'02':"February",'03':"March",'04':"April",'05':"May",'06':"June",'07':"July",'08':"August",'09':"September",'10':"October",'11':"November",'12':"December",}


FULL = """<img src="https://upload.wikimedia.org/wikipedia/commons/3/30/Star-full.png" width="13">"""
EMPTY = """<img src="https://upload.wikimedia.org/wikipedia/commons/7/7a/Star-empty.png" width="13">"""

NoteHtml = {0:EMPTY,
            1:FULL,
            2:FULL+FULL,
            3:FULL+FULL+FULL}

LOGOS = {'NBA':{'BOS':'https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg','BRK':'https://upload.wikimedia.org/wikipedia/commons/4/44/Brooklyn_Nets_newlogo.svg','NYK':'https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg',
'PHI':'https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg','TOR':'https://upload.wikimedia.org/wikipedia/en/3/36/Toronto_Raptors_logo.svg','CHI':'https://upload.wikimedia.org/wikipedia/en/6/67/Chicago_Bulls_logo.svg',
'CLE':'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Cleveland_Cavaliers_logo.svg/800px-Cleveland_Cavaliers_logo.svg.png','DET':'https://upload.wikimedia.org/wikipedia/commons/3/39/Logo_of_the_Detroit_Pistons.png','IND':'https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers.svg',
'MIL':'https://upload.wikimedia.org/wikipedia/en/4/4a/Milwaukee_Bucks_logo.svg','ATL':'https://upload.wikimedia.org/wikipedia/en/2/24/Atlanta_Hawks_logo.svg','CHO':'https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg',
'MIA':'https://upload.wikimedia.org/wikipedia/en/f/fb/Miami_Heat_logo.svg','ORL':'https://upload.wikimedia.org/wikipedia/en/1/10/Orlando_Magic_logo.svg','WAS':'https://upload.wikimedia.org/wikipedia/en/0/02/Washington_Wizards_logo.svg',
'DEN':'https://upload.wikimedia.org/wikipedia/en/7/76/Denver_Nuggets.svg','MIN':'https://upload.wikimedia.org/wikipedia/en/c/c2/Minnesota_Timberwolves_logo.svg','OKC':'https://upload.wikimedia.org/wikipedia/en/5/5d/Oklahoma_City_Thunder.svg',
'POR':'https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg','UTA':'https://upload.wikimedia.org/wikipedia/en/5/52/Utah_Jazz_logo_2022.svg',
'GSW':'https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg','LAC':'https://upload.wikimedia.org/wikipedia/en/b/bb/Los_Angeles_Clippers_%282015%29.svg',
'LAL':'https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg','PHO':'https://upload.wikimedia.org/wikipedia/en/d/dc/Phoenix_Suns_logo.svg','SAC':'https://upload.wikimedia.org/wikipedia/en/c/c7/SacramentoKings.svg',
'DAL':'https://upload.wikimedia.org/wikipedia/en/9/97/Dallas_Mavericks_logo.svg','HOU':'https://upload.wikimedia.org/wikipedia/en/2/28/Houston_Rockets.svg','MEM':'https://upload.wikimedia.org/wikipedia/en/f/f1/Memphis_Grizzlies.svg',
'NOP':'https://upload.wikimedia.org/wikipedia/en/0/0d/New_Orleans_Pelicans_logo.svg','SAS':'https://upload.wikimedia.org/wikipedia/en/a/a2/San_Antonio_Spurs.svg'},
'WNBA':{"ATL":"https://upload.wikimedia.org/wikipedia/en/5/54/Atlanta_Dream_logo.svg","CHI":"https://upload.wikimedia.org/wikipedia/en/f/fc/Chicago_Sky_logo.svg","CON":"https://upload.wikimedia.org/wikipedia/en/0/09/Connecticut_Sun_logo.svg",
"DAL":"https://upload.wikimedia.org/wikipedia/en/9/95/Dallas_Wings_logo.svg","IND":"https://upload.wikimedia.org/wikipedia/en/5/54/Indiana_Fever_logo.svg","LAS":"https://upload.wikimedia.org/wikipedia/en/9/9f/Los_Angeles_Sparks_logo.svg",
"LVA":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Las_Vegas_Aces_logo.svg/800px-Las_Vegas_Aces_logo.svg.png","MIN":"https://upload.wikimedia.org/wikipedia/en/7/75/Minnesota_Lynx_logo.svg","NYL":"https://upload.wikimedia.org/wikipedia/en/a/a1/New_York_Liberty_logo.svg",
"PHO":"https://upload.wikimedia.org/wikipedia/en/a/a6/Phoenix_Mercury_logo.svg","SEA":"https://upload.wikimedia.org/wikipedia/en/a/a0/Seattle_Storm_%282021%29_logo.svg","WAS":"https://upload.wikimedia.org/wikipedia/en/7/79/Washington_Mystics_logo.svg"}
}

TeamsAbbr = {'NBA':{'BOS':'Boston Celtics',
'NYK':'New York Knicks',
'ATL':'Atlanta Hawks',
'BRK':'Brooklyn Nets',
'CHO':'Charlotte Hornets',
'CHI':'Chicago Bulls',
'CLE':'Cleveland Cavaliers',
'DAL':'Dallas Mavericks',
'DEN':'Denver Nuggets',
'DET':'Detroit Pistons',
'GSW':'Golden State Warriors',
'HOU':'Houston Rockets',
'IND':'Indiana Pacers',
'LAC':'Los Angeles Clippers',
'LAL':'Los Angeles Lakers',
'MEM':'Memphis Grizzlies',
'MIA':'Miami Heat',
'MIL':'Milwaukee Bucks',
'MIN':'Minnesota Timberwolves',
'NOP':'New Orleans Pelicans',
'OKC':'Oklahoma City Thunder',
'ORL':'Orlando Magic',
'PHI':'Philadelphia 76ers',
'PHO':'Phoenix Suns',
'POR':'Portland Trail Blazers',
'SAC':'Sacramento Kings',
'SAS':'San Antonio Spurs',
'TOR':'Toronto Raptors',
'UTA':'Utah Jazz',
'WAS':'Washington Wizards'},
'WNBA':{'ATL':'Atlanta Dream','CHI':'Chicago Sky','DAL':'Dallas Wings','LVA':'Las Vegas Aces','PHO':'Phoenix Mercury','SEA':'Seattle Storm',
'MIN':'Minnesota Lynx','WAS':'Washington Mystics','LAS':'Los Angeles Sparks','NYL':'New York Liberty','CON':'Connecticut Sun','IND':'Indiana Fever'}}


aQT = {'NBA':12,'WNBA':10}

ligId = {'NBA':'00','WNBA':'10'}


Leagues = ['NBA','WNBA']

#---
#       FUNCTIONS
#---

def LaSaison(M,Y,L):
    if L == 'NBA':
        if M>=9:return(Y+1)
        else:return(Y)
    elif L == 'WNBA':
        if M>=5:return(Y)
        else:return(Y-1)

def GameName(g,DicoLogo,l):  # dicologo est le dictionnaire correspondant aux teams de la ligue
    matchup = g[4:-4]
    Tm1 = g[:3]
    Tm2 = g[-3:]
    if Tm1 in DicoLogo and Tm2 in DicoLogo:
        if matchup=='@':return('<img src="'+DicoLogo[Tm1]+'" width="15" title="'+TeamsAbbr[l][Tm1]+'">  <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/At_sign.svg" width="10"> <img src="'+DicoLogo[Tm2]+'" width="15" title="'+TeamsAbbr[l][Tm2]+'">')
        if matchup=='vs.':return('<img src="'+DicoLogo[Tm2]+'" width="15" title="'+TeamsAbbr[l][Tm2]+'">  <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/At_sign.svg" width="10"> <img src="'+DicoLogo[Tm1]+'" width="15" title="'+TeamsAbbr[l][Tm1]+'">')
    else:
        if matchup=='@':return(g)
        if matchup=='vs.':return(Tm2+' @ '+Tm1)

def DateEnLettre(d):
    Y = d[:4]
    M = d[5:7]
    D = d[8:]
    return(Lit_Month[M]+' '+Lit_Day[D]+', '+str(Y))
    


def EnSecondes(x):
    min = ''
    carac = 0
    while x[carac]!=':':
        min+=x[carac]
        carac+=1
    sec = x[carac+1:]
    return(int(min)*60+int(sec))
    
def LastTie(temps,margin):
    if margin[-1]>0:
        ind = -1
        while margin[ind]>0:ind-=1
        return(temps[ind]) 
    else:
        ind = -1
        while margin[ind]<0:ind-=1
        return(temps[ind]) 
    
def Last2Pos(temps,margin):
    ind = -1
    while abs(margin[ind])>6:ind-=1
    return(temps[ind])
    
def BigestLead(temps,margin):
    return(np.max([np.max(margin),-1*np.min(margin)]))
        
def BigestLeadLoser(temps,margin):    
    if margin[-1]>0:return(-1*np.min(margin))
    else:
        return(np.max(margin))
    
def VictoryMargin(temps,margin):    
    return(abs(margin[-1]))
    
def OverTime(temps,margin,qt): # qt est le nb de min dans un QT
    return(temps[-1]>4*qt*60)    
    
    
def Stars(temps,margin,lig):        # lig est nba ou wnba
    ot = OverTime(temps,margin,aQT[lig])
    lastie = LastTie(temps,margin)
    efin = VictoryMargin(temps,margin)
    last2pos = Last2Pos(temps,margin)
    cb = BigestLeadLoser(temps,margin)
#    biglead = BigestLead(temps,margin)
    
    lafin = 0
    while temps[lafin]<(4*aQT[lig]-5)*60:lafin+=1
    bigleadSansFin = BigestLead(temps[:lafin],margin[:lafin])
    
    if ot:note = 3
    elif efin>=15 and last2pos<3*aQT[lig]*60:note = 0
    elif lastie>=(4*aQT[lig]-5)*60:
        if efin<=6:note = 3
        else:note = 2
    elif lastie<(4*aQT[lig]-5)*60:
        if efin<=6:
            if cb>=18:note = 3
            else:note = 2
        elif efin<=10:
            if cb>=18:
                if last2pos>=(4*aQT[lig]-2.5)*60:note = 3
                else:note = 2
            else:
                if last2pos>=(4*aQT[lig]-2.5)*60:note = 2
                else:note = 1
        elif efin>10:
            if cb>=18:note = 2
            else:
                if last2pos>=(4*aQT[lig]-2.5)*60:note = 2
                else:note = 1

    if bigleadSansFin<=10 and note<3:note+=1
    return(note)
    
    
# Functions to scrap basketball reference for the NBA
def get_schedule(season, playoffs=False):
    months = ['October', 'November', 'December', 'January', 'February', 'March',
            'April', 'May', 'June']
    if season==2020:
        months = ['October-2019', 'November', 'December', 'January', 'February', 'March',
                'July', 'August', 'September', 'October-2020']
    df = pd.DataFrame()
    for month in months:
        r = get(f'https://www.basketball-reference.com/leagues/NBA_{season}_games-{month.lower()}.html')
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', attrs={'id': 'schedule'})
            if table:
                month_df = pd.read_html(str(table))[0]
                df = pd.concat([df, month_df])

    df = df.reset_index()

    cols_to_remove = [i for i in df.columns if 'Unnamed' in i]
    cols_to_remove += [i for i in df.columns if 'Notes' in i]
    cols_to_remove += [i for i in df.columns if 'Start' in i]
    cols_to_remove += [i for i in df.columns if 'Attend' in i]
    cols_to_remove += [i for i in df.columns if 'Arena' in i]
    cols_to_remove += ['index']
    df = df.drop(cols_to_remove, axis=1)
    df.columns = ['DATE', 'VISITOR', 'VISITOR_PTS', 'HOME', 'HOME_PTS']

    if season==2020:
        df = df[df['DATE']!='Playoffs']
        df['DATE'] = df['DATE'].apply(lambda x: pd.to_datetime(x))
        df = df.sort_values(by='DATE')
        df = df.reset_index().drop('index', axis=1)
        playoff_loc = df[df['DATE']==pd.to_datetime('2020-08-17')].head(n=1)
        if len(playoff_loc.index)>0:
            playoff_index = playoff_loc.index[0]
        else:
            playoff_index = len(df)
        if playoffs:
            df = df[playoff_index:]
        else:
            df = df[:playoff_index]
    else:
        # account for 1953 season where there's more than one "playoffs" header
        if season == 1953:
            df.drop_duplicates(subset=['DATE', 'HOME', 'VISITOR'], inplace=True)
        playoff_loc = df[df['DATE']=='Playoffs']
        if len(playoff_loc.index)>0:
            playoff_index = playoff_loc.index[0]
        else:
            playoff_index = len(df)
        if playoffs:
            df = df[playoff_index+1:]
        else:
            df = df[:playoff_index]
        df['DATE'] = df['DATE'].apply(lambda x: pd.to_datetime(x))
    return df

    
def get_pbp_helper(suffix):
    r = get(f'https://www.basketball-reference.com/boxscores/pbp{suffix}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', attrs={'id': 'pbp'})
        return pd.read_html(str(table))[0]

        
def format_df(df1):
    df1.columns = list(map(lambda x: x[1], list(df1.columns)))
    t1 = list(df1.columns)[1].upper()
    t2 = list(df1.columns)[5].upper()
    q = 1
    df = None
    for index, row in df1.iterrows():
        d = {'QUARTER': float('nan'), 'TIME_REMAINING': float('nan'), f'{t1}_ACTION': float('nan'), f'{t2}_ACTION': float('nan'), f'{t1}_SCORE': float('nan'), f'{t2}_SCORE': float('nan')}
        if row['Time']=='2nd Q':
            q = 2
        elif row['Time']=='3rd Q':
            q = 3
        elif row['Time']=='4th Q':
            q = 4
        elif 'OT' in row['Time']:
            q = row['Time'][0]+'OT'
        try:
            d['QUARTER'] = q
            d['TIME_REMAINING'] = row['Time']
            scores = row['Score'].split('-')
            d[f'{t1}_SCORE'] = int(scores[0])
            d[f'{t2}_SCORE'] = int(scores[1])
            d[f'{t1}_ACTION'] = row[list(df1.columns)[1]]
            d[f'{t2}_ACTION'] = row[list(df1.columns)[5]]
            if df is None:
                df = pd.DataFrame(columns = list(d.keys()))
            df = df.append(d, ignore_index=True)
        except:
            continue
    return df

def get_pbp(date, team1, team2):
    suffix = get_game_suffix(date, team1, team2)#.replace('/boxscores', '')
    date = pd.to_datetime(date)
    df = get_pbp_helper(suffix)
    df = format_df(df)
    return df      

# Functions to scrap basketball reference for the WNBA
def get_schedule_WNBA(season, playoffs=False):
    df = pd.DataFrame()
    r = get(f'https://www.basketball-reference.com/wnba/years/{season}_games.html')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', attrs={'id': 'schedule'})
        if table:
            month_df = pd.read_html(str(table))[0]
            df = pd.concat([df, month_df])

    df = df.reset_index()

    cols_to_remove = [i for i in df.columns if 'Unnamed' in i]
    cols_to_remove += [i for i in df.columns if 'Notes' in i]
    cols_to_remove += [i for i in df.columns if 'Start' in i]
    cols_to_remove += [i for i in df.columns if 'Attend' in i]
    cols_to_remove += [i for i in df.columns if 'Arena' in i]
    cols_to_remove += ['index']
    df = df.drop(cols_to_remove, axis=1)
    df.columns = ['DATE', 'VISITOR', 'VISITOR_PTS', 'HOME', 'HOME_PTS']

    if season==2020:
        df = df[df['DATE']!='Playoffs']
        df['DATE'] = df['DATE'].apply(lambda x: pd.to_datetime(x))
        df = df.sort_values(by='DATE')
        df = df.reset_index().drop('index', axis=1)
        playoff_loc = df[df['DATE']==pd.to_datetime('2020-08-17')].head(n=1)
        if len(playoff_loc.index)>0:
            playoff_index = playoff_loc.index[0]
        else:
            playoff_index = len(df)
        if playoffs:
            df = df[playoff_index:]
        else:
            df = df[:playoff_index]
    else:
        # account for 1953 season where there's more than one "playoffs" header
        if season == 1953:
            df.drop_duplicates(subset=['DATE', 'HOME', 'VISITOR'], inplace=True)
        playoff_loc = df[df['DATE']=='Playoffs']
        if len(playoff_loc.index)>0:
            playoff_index = playoff_loc.index[0]
        else:
            playoff_index = len(df)
        if playoffs:
            df = df[playoff_index+1:]
        else:
            df = df[:playoff_index]
        df['DATE'] = df['DATE'].apply(lambda x: pd.to_datetime(x))
    return df

def get_game_suffix_WNBA(date, team1, team2):
    return('/'+date[0:4]+date[5:7]+date[8:10]+'0'+team2+".html")
    
def get_game_suffix(date, team1, team2):
    return('/'+date[0:4]+date[5:7]+date[8:10]+'0'+team2+".html")

def get_pbp_WNBA_helper_WNBA(suffix):
    r = get(f'https://www.basketball-reference.com/wnba/boxscores/pbp{suffix}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', attrs={'id': 'pbp'})
        return pd.read_html(str(table))[0]

def format_df_WNBA(df1):
    df1.columns = list(map(lambda x: x[1], list(df1.columns)))
    t1 = list(df1.columns)[1].upper()
    t2 = list(df1.columns)[5].upper()
    q = 1
    df = None
    for index, row in df1.iterrows():
        d = {'QUARTER': float('nan'), 'TIME_REMAINING': float('nan'), f'{t1}_ACTION': float('nan'), f'{t2}_ACTION': float('nan'), f'{t1}_SCORE': float('nan'), f'{t2}_SCORE': float('nan')}
        if row['Time']=='2nd Q':
            q = 2
        elif row['Time']=='3rd Q':
            q = 3
        elif row['Time']=='4th Q':
            q = 4
        elif 'OT' in row['Time']:
            q = row['Time'][0]+'OT'
        try:
            d['QUARTER'] = q
            d['TIME_REMAINING'] = row['Time']
            scores = row['Score'].split('-')
            d[f'{t1}_SCORE'] = int(scores[0])
            d[f'{t2}_SCORE'] = int(scores[1])
            d[f'{t1}_ACTION'] = row[list(df1.columns)[1]]
            d[f'{t2}_ACTION'] = row[list(df1.columns)[5]]
            if df is None:
                df = pd.DataFrame(columns = list(d.keys()))
            df = df.append(d, ignore_index=True)
        except:
            continue
    return df

def get_pbp_WNBA(date, team1, team2):
    suffix = get_game_suffix_WNBA(date, team1, team2)#.replace('/boxscores', '')
    date = pd.to_datetime(date)
    df = get_pbp_WNBA_helper_WNBA(suffix)
    df = format_df_WNBA(df)
    return df

def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days[1:]

Functions = {'NBA':[get_schedule,get_pbp],'WNBA':[get_schedule_WNBA,get_pbp_WNBA]}

# --- Get Last time run
with open("date.txt","r", encoding="utf-8") as f:
    lines = [line.strip().split("XXX") for line in f]
Last = datetime.strptime(lines[0][0], '%m/%d/%Y')
    
# --- Get yesterday date
Yesterday = datetime.now() - timedelta(1)

# --- Put the date correctly formated
YestWrite = datetime.strftime(Yesterday,"%m/%d/%Y")

# --- Write the date in a file
FileDate = open("date.txt","w") 
FileDate.write(YestWrite)
FileDate.close()

# --- Get the schedules from the API
SeasonApiExtracted = {}
for league in Leagues:
    # --- Get the season's last year
    Year = {'NBA':LaSaison(int(datetime.strftime(Yesterday,"%m")),int(datetime.strftime(Yesterday,"%Y")),'NBA'),'WNBA':LaSaison(int(datetime.strftime(Yesterday,"%m")),int(datetime.strftime(Yesterday,"%Y")),'WNBA')}
    
    # --- Request the games of the current season
    dextr = Functions[league][0](Year[league])
    
    # --- Get the playoffs games for the WNBA
    if league=='WNBA':
        d_PO = Functions[league][0](Year[league],True)
        frames = [dextr, d_PO]
        dextr = pd.concat(frames,ignore_index=True)
    
    SeasonApiExtracted[league] = dextr


# --- Evaluate the days between last run    
LesDates = date_range(Last, Yesterday)
LesDates = [Yesterday]

for ld in LesDates:
    
    # --- Get what's already in the Notes file
    with open("index.md","r", encoding="utf-8") as f:
        lines = [line.strip().split("XXX") for line in f]    
    
    file = open("index.md","w") 
    file.write(lines[0][0]+'\n')

    if int(datetime.strftime(ld,"%m")) not in [5,6,7,8,9]: Leagues = ['NBA'] # on s'interesse only a la NBA if not btw May and Sept    
    for league in Leagues:
        Today = ld
        
        TeamsAbbr_inv = {TeamsAbbr[league][x]:x for x in TeamsAbbr[league]}
        
        d = SeasonApiExtracted[league]
                
        # --- Put the date correctly formated
        Today = datetime.strftime(Today,"%m/%d/%Y")
        
#        # --- Write the date in a file
#        FileDate = open("date.txt","w") 
#        FileDate.write(Today)
#        FileDate.close()
        
        # --- Récuperer les indices des matchs de la nuit derniere
        GameDates = []
        Dates = list(d['DATE'])
        for i in range(0,len(Dates)):
            LaDate = datetime.strftime(Dates[i].to_pydatetime(),"%m/%d/%Y")
            if LaDate==Today:GameDates.append(i)
        
        
        for Game in  GameDates[0:1]:
            LaDate = datetime.strftime(d['DATE'][Game],"%Y-%m-%d")
            Team_Vis = TeamsAbbr_inv[d['VISITOR'][Game]]
            Team_Dom = TeamsAbbr_inv[d['HOME'][Game]]
            
            Suffix = get_game_suffix(LaDate,Team_Vis,Team_Dom)
            DDD = get_pbp_helper(Suffix)
            print(DDD)
            
            
            DDD.columns = list(map(lambda x: x[1], list(DDD.columns)))
            t1 = list(DDD.columns)[1].upper()
            t2 = list(DDD.columns)[5].upper()
            q = 1
            DF = None
            for index, row in DDD.iterrows():
                d = {'QUARTER': float('nan'), 'TIME_REMAINING': float('nan'), f'{t1}_ACTION': float('nan'), f'{t2}_ACTION': float('nan'), f'{t1}_SCORE': float('nan'), f'{t2}_SCORE': float('nan')}
                if row['Time']=='2nd Q':
                    q = 2
                elif row['Time']=='3rd Q':
                    q = 3
                elif row['Time']=='4th Q':
                    q = 4
                elif 'OT' in row['Time']:
                    q = row['Time'][0]+'OT'
                try:
                    d['QUARTER'] = q
                    d['TIME_REMAINING'] = row['Time']
                    scores = row['Score'].split('-')
                    d[f'{t1}_SCORE'] = int(scores[0])
                    d[f'{t2}_SCORE'] = int(scores[1])
                    d[f'{t1}_ACTION'] = row[list(DDD.columns)[1]]
                    d[f'{t2}_ACTION'] = row[list(DDD.columns)[5]]
                    if DF is None:
                        DF = pd.DataFrame(columns = list(d.keys()))
                    DF = DF.append(d, ignore_index=True)

                    print('----------')
                    print(DF)
                    print('##########')
                except:
                    continue
            
            print(DF)
            
            # --- Get the Play by play score evolution
            Period = [1]
            Timer = [aQT[league]*60]
            ScoreMargin = [0]
            NbAction = len(DF[list(DF)[0]])
            for i in range (0,NbAction):
                if ':' in DF['TIME_REMAINING'][i][:-2]: 
                    Period.append(DF['QUARTER'][i])
                    Timer.append(EnSecondes(DF['TIME_REMAINING'][i][:-2]))
                # --- boucle pour toujours faire score vainqueur - score loser
                if DF[list(DF)[4]][NbAction-1]>DF[list(DF)[5]][NbAction-1]:       
                    ScoreMargin.append(DF[list(DF)[4]][i]-DF[list(DF)[5]][i])
                else :
                    ScoreMargin.append(DF[list(DF)[5]][i]-DF[list(DF)[4]][i])
            Period.append(Period[-1])
            Timer.append(0)
            ScoreMargin.append(ScoreMargin[-1])
            
            # --- Artificially rewrite the Period list because it can have some bug in the scrap
            NewPeriod = [1]
            leQT = 1
            for i in range(1,len(Timer)):
                if Timer[i-1]<Timer[i]:leQT+=1
                NewPeriod.append(leQT)
            Period = NewPeriod        
            
            # --- To add 12:00 and 00:00 in between the QT
            i = 1
            while i < len(Period)-1:
                if Timer[i]>Timer[i-1]:
                    Period.insert(i,Period[i-1])
                    Period.insert(i+1,Period[i-1]+1)
                    Timer.insert(i,0)
                    if Period[i-1]<=4:Timer.insert(i+1,aQT[league]*60)
                    else:Timer.insert(i+1,300)
                    ScoreMargin.insert(i,ScoreMargin[i-1])
                    ScoreMargin.insert(i+1,ScoreMargin[i-1])
                    i+=2
                i+=1
            
            # --- Correct the Period list if there is overtime
            for it in range(0,len(Period)):
                if type(Period[it])==str:
                    Period[it]=4+int(Period[it][0])
                    
            # --- Correct the timer to put it in overall seconds
            OverallTimer = []
            for j in range(0,len(Timer)):
                Decal = sum([Timer[Period.index(x)] for x in range(1,Period[j])])
                OverallTimer.append(Decal+Timer[Period.index(Period[j])]-Timer[j])
            
            # --- Calculate the useful values         
            last_tie = LastTie(OverallTimer,ScoreMargin)
            last_2_pos = Last2Pos(OverallTimer,ScoreMargin)
            biggest_lead_loser = BigestLeadLoser(OverallTimer,ScoreMargin)
            biggest_lead = BigestLead(OverallTimer,ScoreMargin)    
            victory_margin = VictoryMargin(OverallTimer,ScoreMargin)   
            overtime = OverTime(OverallTimer,ScoreMargin,aQT[league])
            lanote = Stars(OverallTimer,ScoreMargin,league)
        
        
        
        #    file.write(Date+' '+Matchup+' '+str(lanote)+'\n')
            file.write('<tr><td style="text-align:center">'+DateEnLettre(LaDate)+'</td><td style="text-align:center">'+GameName(Team_Vis+' @ '+Team_Dom,LOGOS[league],league)+'</td><td style="text-align:center">'+NoteHtml[lanote]+'</td></tr>\n')
    
        
    if len(lines)>201:
        for l in lines[1:200]:file.write(l[0]+'\n')
        file.write(lines[-1][0]+'\n')
    else:
        for l in lines[1:]:file.write(l[0]+'\n')    
        
    file.close()
            
# --- Get if it was run today
Checkfile = open("Check.txt","w")
Checkfile.write(str(Yesterday.hour))
Checkfile.close

    
