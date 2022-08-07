#---
#       IMPORT LIBRARIES
#---

import numpy as np
from datetime import datetime, timedelta
from basketball_reference_scraper.seasons import get_schedule
from basketball_reference_scraper.pbp import get_pbp


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
'CLE':'https://upload.wikimedia.org/wikipedia/en/4/4b/Cleveland_Cavaliers_logo.svg','DET':'https://upload.wikimedia.org/wikipedia/commons/7/7c/Pistons_logo17.svg','IND':'https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers.svg',
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
"LVA":"https://upload.wikimedia.org/wikipedia/en/f/fb/Las_Vegas_Aces_logo.svg","MIN":"https://upload.wikimedia.org/wikipedia/en/7/75/Minnesota_Lynx_logo.svg","NYL":"https://upload.wikimedia.org/wikipedia/en/a/a1/New_York_Liberty_logo.svg",
"PHO":"https://upload.wikimedia.org/wikipedia/en/a/a6/Phoenix_Mercury_logo.svg","SEA":"https://upload.wikimedia.org/wikipedia/en/a/a0/Seattle_Storm_%282021%29_logo.svg","WAS":"https://upload.wikimedia.org/wikipedia/en/7/79/Washington_Mystics_logo.svg"}
}

TeamsAbbr = {'BOS':'Boston Celtics',
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
'WAS':'Washington Wizards'
}

TeamsAbbr_inv = {TeamsAbbr[x]:x for x in TeamsAbbr}


aQT = {'NBA':12,'WNBA':10}

ligId = {'NBA':'00','WNBA':'10'}


Leagues = ['NBA','WNBA']

#---
#       FUNCTIONS
#---


def LaSaison(M,Y):
    if M>=9:return(Y+1)
    else:return(Y)

def GameName(g,DicoLogo):  # dicologo est le dictionnaire correspondant aux teams de la ligue
    matchup = g[4:-4]
    Tm1 = g[:3]
    Tm2 = g[-3:]
    if Tm1 in DicoLogo and Tm2 in DicoLogo:
        if matchup=='@':return('<img src="'+DicoLogo[Tm1]+'" width="15" title="'+TeamsAbbr[Tm1]+'">  <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/At_sign.svg" width="10"> <img src="'+DicoLogo[Tm2]+'" width="15" title="'+TeamsAbbr[Tm2]+'">')
        if matchup=='vs.':return('<img src="'+DicoLogo[Tm2]+'" width="15" title="'+TeamsAbbr[Tm2]+'">  <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/At_sign.svg" width="10"> <img src="'+DicoLogo[Tm1]+'" width="15" title="'+TeamsAbbr[Tm1]+'">')
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


# --- Get yesterday date
Today = datetime.now() - timedelta(1)


# --- Get the season's last year
Year = LaSaison(int(datetime.strftime(Today,"%m")),int(datetime.strftime(Today,"%Y")))

# --- Request the games of the current season
d = get_schedule(Year)

# --- Put the date correctly formated
Today = datetime.strftime(Today,"%m/%d/%Y")

# --- Write the date in a file
FileDate = open("date.txt","w") 
FileDate.write(Today)
FileDate.close()

# --- Récuperer les indices des matchs de la nuit derniere
GameDates = []
Dates = list(d['DATE'])
for i in range(0,len(Dates)):
    LaDate = datetime.strftime(Dates[i].to_pydatetime(),"%m/%d/%Y")
    if LaDate==Today:GameDates.append(i)

league = 'NBA'

# --- Get what's already in the Notes file
with open("index.md","r", encoding="utf-8") as f:
    lines = [line.strip().split("XXX") for line in f]    

file = open("index.md","w") 
file.write(lines[0][0]+'\n')


for Game in  GameDates:
    LaDate = datetime.strftime(d['DATE'][Game],"%Y-%m-%d")
    Team_Vis = TeamsAbbr_inv[d['VISITOR'][Game]]
    Team_Dom = TeamsAbbr_inv[d['HOME'][Game]]
    df = get_pbp(LaDate,Team_Vis,Team_Dom)

    # --- Get the Play by play score evolution
    Period = [1]
    Timer = [aQT[league]*60]
    ScoreMargin = [0]
    NbAction = len(df[list(df)[0]])
    for i in range (0,NbAction):
        Period.append(df['QUARTER'][i])
        Timer.append(EnSecondes(df['TIME_REMAINING'][i][:-2]))
        # --- boucle pour toujours faire score vainqueur - score loser
        if df[list(df)[4]][NbAction-1]>df[list(df)[5]][NbAction-1]:       
            ScoreMargin.append(df[list(df)[4]][i]-df[list(df)[5]][i])
        else :
            ScoreMargin.append(df[list(df)[5]][i]-df[list(df)[4]][i])
    Period.append(Period[-1])
    Timer.append(0)
    ScoreMargin.append(ScoreMargin[-1])
    
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
    file.write('<tr><td style="text-align:center">'+DateEnLettre(LaDate)+'</td><td style="text-align:center">'+GameName(Team_Vis+' @ '+Team_Dom,LOGOS[league])+'</td><td style="text-align:center">'+NoteHtml[lanote]+'</td></tr>\n')

    
if len(lines)>201:
    for l in lines[1:200]:file.write(l[0]+'\n')
    file.write(lines[-1][0]+'\n')
else:
    for l in lines[1:]:file.write(l[0]+'\n')    
    
file.close()

    
