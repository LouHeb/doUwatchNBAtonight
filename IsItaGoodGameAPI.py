#---
#       IMPORT LIBRARIES
#---

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from datetime import datetime, timedelta
import time 

#plt.close('all')
custom_headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language' = 'en-US,en;q=0.8,af;q=0.6'
}


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

LOGOS = {'NBA':{'BOS':'https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg','BKN':'https://upload.wikimedia.org/wikipedia/commons/4/44/Brooklyn_Nets_newlogo.svg','NYK':'https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg',
'PHI':'https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg','TOR':'https://upload.wikimedia.org/wikipedia/en/3/36/Toronto_Raptors_logo.svg','CHI':'https://upload.wikimedia.org/wikipedia/en/6/67/Chicago_Bulls_logo.svg',
'CLE':'https://upload.wikimedia.org/wikipedia/en/4/4b/Cleveland_Cavaliers_logo.svg','DET':'https://upload.wikimedia.org/wikipedia/commons/7/7c/Pistons_logo17.svg','IND':'https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers.svg',
'MIL':'https://upload.wikimedia.org/wikipedia/en/4/4a/Milwaukee_Bucks_logo.svg','ATL':'https://upload.wikimedia.org/wikipedia/en/2/24/Atlanta_Hawks_logo.svg','CHA':'https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg',
'MIA':'https://upload.wikimedia.org/wikipedia/en/f/fb/Miami_Heat_logo.svg','ORL':'https://upload.wikimedia.org/wikipedia/en/1/10/Orlando_Magic_logo.svg','WAS':'https://upload.wikimedia.org/wikipedia/en/0/02/Washington_Wizards_logo.svg',
'DEN':'https://upload.wikimedia.org/wikipedia/en/7/76/Denver_Nuggets.svg','MIN':'https://upload.wikimedia.org/wikipedia/en/c/c2/Minnesota_Timberwolves_logo.svg','OKC':'https://upload.wikimedia.org/wikipedia/en/5/5d/Oklahoma_City_Thunder.svg',
'POR':'https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg','UTA':'https://upload.wikimedia.org/wikipedia/en/5/52/Utah_Jazz_logo_2022.svg',
'GSW':'https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg','LAC':'https://upload.wikimedia.org/wikipedia/en/b/bb/Los_Angeles_Clippers_%282015%29.svg',
'LAL':'https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg','PHX':'https://upload.wikimedia.org/wikipedia/en/d/dc/Phoenix_Suns_logo.svg','SAC':'https://upload.wikimedia.org/wikipedia/en/c/c7/SacramentoKings.svg',
'DAL':'https://upload.wikimedia.org/wikipedia/en/9/97/Dallas_Mavericks_logo.svg','HOU':'https://upload.wikimedia.org/wikipedia/en/2/28/Houston_Rockets.svg','MEM':'https://upload.wikimedia.org/wikipedia/en/f/f1/Memphis_Grizzlies.svg',
'NOP':'https://upload.wikimedia.org/wikipedia/en/0/0d/New_Orleans_Pelicans_logo.svg','SAS':'https://upload.wikimedia.org/wikipedia/en/a/a2/San_Antonio_Spurs.svg'},
'WNBA':{"ATL":"https://upload.wikimedia.org/wikipedia/en/5/54/Atlanta_Dream_logo.svg","CHI":"https://upload.wikimedia.org/wikipedia/en/f/fc/Chicago_Sky_logo.svg","CON":"https://upload.wikimedia.org/wikipedia/en/0/09/Connecticut_Sun_logo.svg",
"DAL":"https://upload.wikimedia.org/wikipedia/en/9/95/Dallas_Wings_logo.svg","IND":"https://upload.wikimedia.org/wikipedia/en/5/54/Indiana_Fever_logo.svg","LAS":"https://upload.wikimedia.org/wikipedia/en/9/9f/Los_Angeles_Sparks_logo.svg",
"LVA":"https://upload.wikimedia.org/wikipedia/en/f/fb/Las_Vegas_Aces_logo.svg","MIN":"https://upload.wikimedia.org/wikipedia/en/7/75/Minnesota_Lynx_logo.svg","NYL":"https://upload.wikimedia.org/wikipedia/en/a/a1/New_York_Liberty_logo.svg",
"PHO":"https://upload.wikimedia.org/wikipedia/en/a/a6/Phoenix_Mercury_logo.svg","SEA":"https://upload.wikimedia.org/wikipedia/en/a/a0/Seattle_Storm_%282021%29_logo.svg","WAS":"https://upload.wikimedia.org/wikipedia/en/7/79/Washington_Mystics_logo.svg"}
}

aQT = {'NBA':12,'WNBA':10}

ligId = {'NBA':'00','WNBA':'10'}


Leagues = ['WNBA','NBA']

#---
#       FUNCTIONS
#---

def GameName(g,DicoLogo):  # dicologo est le dictionnaire correspondant aux teams de la ligue
    matchup = g[4:-4]
    Tm1 = g[:3]
    Tm2 = g[-3:]
    if Tm1 in DicoLogo and Tm2 in DicoLogo:
        if matchup=='@':return('<img src="'+DicoLogo[Tm1]+'" width="15">  <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/At_sign.svg" width="10"> <img src="'+DicoLogo[Tm2]+'" width="15">')
        if matchup=='vs.':return('<img src="'+DicoLogo[Tm2]+'" width="15">  <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/At_sign.svg" width="10"> <img src="'+DicoLogo[Tm1]+'" width="15">')
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


# --- Get yesterday's date
Today = datetime.strftime(datetime.now() - timedelta(1),"%m/%d/%Y")
#Today = "06/16/2022"

from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playbyplay


for league in Leagues:
    
    # --- Extract the games of yesterday
    StudiedGames = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation='T',date_from_nullable = Today,date_to_nullable = Today, league_id_nullable = ligId[league], outcome_nullable = "W", headers=custom_headers)
    #StudiedGames = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation='T',season_nullable = '2021-22', league_id_nullable = ligId[league], outcome_nullable = "W")
    
    df = StudiedGames.get_data_frames()
    time.sleep(0.5)    

    # --- Get what's already in the Notes file
    with open("index.md","r", encoding="utf-8") as f:
        lines = [line.strip().split("XXX") for line in f]
        
    # --- Calculate the Note for each game of today
    file = open("index.md","w") 
    file.write(lines[0][0]+'\n')
    for Index in range(0,len(df[0]['GAME_ID'])):
        LeGame = df[0]['GAME_ID'][Index]
        Matchup = df[0]['MATCHUP'][Index]
        Date = df[0]['GAME_DATE'][Index]
        
        # --- Extract the play-by-play of this game
        pbp = playbyplay.PlayByPlay(game_id=LeGame, headers=custom_headers)
        dfPBP = pbp.get_data_frames()
        time.sleep(0.5)
            
        # --- Extract the Timer, QT and score margin
        Period = [int(dfPBP[0]["PERIOD"][0])]
        Timer = [EnSecondes(dfPBP[0]["PCTIMESTRING"][0])]
        ScoreMargin = [0]
        for event in range(1,len(dfPBP[0]['GAME_ID'])):
            Period.append(int(dfPBP[0]["PERIOD"][event]))
            Timer.append(EnSecondes(dfPBP[0]["PCTIMESTRING"][event]))
            LeScore = dfPBP[0]["SCOREMARGIN"][event]
            if LeScore == None:
                ScoreMargin.append(ScoreMargin[-1])
            elif LeScore == 'TIE':
                ScoreMargin.append(0)
            else:
                ScoreMargin.append(int(LeScore))
        
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
        file.write('<tr><td style="text-align:center">'+DateEnLettre(Date)+'</td><td style="text-align:center">'+GameName(Matchup,LOGOS[league])+'</td><td style="text-align:center">'+NoteHtml[lanote]+'</td></tr>\n')
    
    
    
    
        # --- Calculate the derivative of the score margin
        PtPerSec = []
        for j in range (0,len(OverallTimer)):
            Remainin = OverallTimer[-1]-OverallTimer[j]
            Ecart = ScoreMargin[j]
            if Remainin!=0:PtPerSec.append(Ecart*60/Remainin)
        
        End = OverallTimer[-1]
        while OverallTimer[-1]==End:
            del OverallTimer[-1]
            
    #    # --- Plot the score evolution
    #    fig, ax = plt.subplots(2,1)
    #    fig.set_figheight(10)
    #    fig.set_figwidth(10)
    #    ax[0].plot(OverallTimer,ScoreMargin,'k')
    #    
    #    ax[0].set_title(Matchup+' on '+Date+' - id'+LeGame,fontsize = 15)
    #    if Matchup[4]=='@':
    #        ax[0].text(-150,0.5,Matchup[-3:],color = 'salmon')
    #        ax[0].text(-150,-1,Matchup[:3],color = 'salmon')
    #    else:
    #        ax[0].text(-150,0.5,Matchup[:3],color = 'salmon')
    #        ax[0].text(-150,-1,Matchup[-3:],color = 'salmon')    
    #    ax[0].plot([-150,0],[0,0],':',color='salmon')
    #    ax[0].plot([0,OverallTimer[-1]],[0,0],'salmon')
    #    for j in range(2,Period[-1]+1):
    #        Decal = sum([Timer[Period.index(x)] for x in range(1,j)])
    #        ax[0].plot([Decal,Decal],[np.min(ScoreMargin),np.max(ScoreMargin)],'salmon')
    #    ax[0].grid(axis='y')
    #    ax[0].axis([-50,OverallTimer[-1]+50,-15,15])
    #    ax[0].set_xlabel('Time (sec)',fontsize = 15)
    #    ax[0].set_ylabel('Ecart',fontsize = 15)
    #    ax[0].text(0,20,'EcartFinal:'+str(victory_margin),color = 'salmon')
    #    ax[0].text(500,20,'OT ?:'+str(overtime),color = 'salmon')
    #    ax[0].text(1000,20,'LastTie:'+str(last_tie//60)+':'+str(last_tie%60),color = 'salmon')
    #    ax[0].text(1500,20,'Last2Po:'+str(last_2_pos//60)+':'+str(last_2_pos%60),color = 'salmon')
    #    ax[0].text(2000,20,'BigLeadLoser:'+str(biggest_lead_loser),color = 'salmon')
    #    ax[0].text(2500,20,'BigLead:'+str(biggest_lead),color = 'salmon')
    #    ax[0].text(0,17.5,'Note = '+str(lanote),color = 'red')
    #    
    #    ax[1].plot(OverallTimer,PtPerSec,'g')
    #
    #    ax[1].grid(axis='y')
    #    ax[1].axis([-50,OverallTimer[-1]+50,-5,5])
    #    ax[1].set_xlabel('Time (sec)',fontsize = 15)
    #    ax[1].set_ylabel('Pts per Min to egalize',fontsize = 15)
    #    fig.savefig(Date+Matchup+'.png')
    #    plt.close()
    
    if len(lines)>201:
        for l in lines[1:200]:file.write(l[0]+'\n')
        file.write(lines[-1][0]+'\n')
    else:
        for l in lines[1:]:file.write(l[0]+'\n')    
        
    #file.write(</table></center><br><center><img src="https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg" width="70"></center></html><center><script type='text/javascript' src='https://www.freevisitorcounters.com/auth.php?id=b549e3c4b028c3fa45765f9028b5a850f0e8bb22'></script><script type="text/javascript" src="https://www.freevisitorcounters.com/en/home/counter/954972/t/3"></script></center></html>')
    file.close()
    
    
    
    
    
    ## --- Write an extraction in a text file
    #file = open("DATA.txt","w") 
    #for col in dfPBP[0]:
    #    file.write(col+'\t')
    #file.write('\n')
    #for game in range(0,len(dfPBP[0]['GAME_ID'])):
    #    for col in dfPBP[0]:
    #        file.write(str(dfPBP[0][col][game])+'\t')
    #    file.write('\n')
    #file.close()

