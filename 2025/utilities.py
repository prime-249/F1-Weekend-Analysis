import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

team_colors = {
    "Alpine": "#F282B4",       # Pink
    "Aston Martin": "#037A68", # Green
    "Ferrari": "#821729",      # Burgundy
    "Haas F1 Team": "#EB0A1E",         # Red
    "Kick Sauber": "#53FC18",  # Bright Green
    "McLaren": "#FF8700",      # Papaya Orange
    "Mercedes": "#C8CCCE",     # Silver/Gray
    "Racing Bulls": "#FFFFFF", # White
    "Red Bull Racing": "#003773",     # Navy Blue
    "Williams": "#00A0DE",     # Blue
}
driver_colors = {
    # Red Bull Racing
    "VER": "#002D5A",  # Max Verstappen (Deep Navy Blue)
    "TSU": "#003F7D",  # Liam Lawson (Brighter Blue)

    # Ferrari
    "LEC": "#9B1B30",  # Charles Leclerc (Darker Burgundy)
    "HAM": "#C81D37",  # Lewis Hamilton (Brighter Red)

    # Mercedes
    "RUS": "#ACB2B5",  # George Russell (Dark Silver)
    "ANT": "#D0D3D4",  # Andrea Kimi Antonelli (Lighter Silver)

    # McLaren
    "NOR": "#FF9800",  # Lando Norris (Papaya Orange)
    "PIA": "#FFB766",  # Oscar Piastri (Lighter Papaya)

    # Aston Martin
    "ALO": "#028061",  # Fernando Alonso (Dark Green)
    "STR": "#03A678",  # Lance Stroll (Lighter Green)

    # Alpine
    "GAS": "#FF66A1",  # Pierre Gasly (Light Pink)
    "DOO": "#D94A90",  # Jack Doohan (Darker Pink)

    # Williams
    "ALB": "#0096C9",  # Alexander Albon (Deep Blue)
    "SAI": "#00B6F1",  # Carlos Sainz (Sky Blue)

    # Racing Bulls
    "HAD": "#E5E5E5",  # Isack Hadjar (Light Gray)
    "LAW": "#F2F2F2",  # Yuki Tsunoda (White)

    # Kick Sauber
    "HUL": "#4EF535",  # Nico Hülkenberg (Bright Green)
    "BOR": "#26D401",  # Gabriel Bortoleto (Darker Green)

    # Haas
    "OCO": "#D91A26",  # Esteban Ocon (Dark Red)
    "BEA": "#F52439",  # Oliver Bearman (Brighter Red)
}
driver_colors_2 = {
    # Red Bull Racing
    "VER": "#003366",  # Slightly darker navy blue
    "TSU": "#004B8D",  # Slightly darker blue

    # Ferrari
    "LEC": "#8B192B",  # Slightly darker burgundy
    "HAM": "#D32F45",  # Slightly lighter/brighter red

    # Mercedes
    "RUS": "#A0A5A8",  # Slightly darker silver
    "ANT": "#D9DDDE",  # Slightly lighter silver

    # McLaren
    "NOR": "#FF8A00",  # Slightly darker orange
    "PIA": "#FFC177",  # Slightly lighter orange

    # Aston Martin
    "ALO": "#026E55",  # Slightly darker green
    "STR": "#04B386",  # Slightly lighter/brighter green

    # Alpine
    "GAS": "#FF75AC",  # Slightly lighter pink
    "DOO": "#C74383",  # Slightly darker pink

    # Williams
    "ALB": "#0088B5",  # Slightly darker blue
    "SAI": "#00C2FF",  # Slightly lighter blue

    # Racing Bulls
    "HAD": "#DCDCDC",  # Slightly darker gray
    "LAW": "#FFFFFF",  # Slightly darker white

    # Kick Sauber
    "HUL": "#46DC2F",  # Slightly darker green
    "BOR": "#2EE001",  # Slightly lighter green

    # Haas
    "OCO": "#C11722",  # Slightly darker red
    "BEA": "#FF2E45",  # Slightly brighter red
}
compound_colors = {
    'SOFT':'#FF0000',
    'MEDIUM':'#FFFF00',
    'HARD':'#808080'
}

def GetGapsInRace(input_df):
    '''
    Generate new column containing the gap from the driver in front at the start of the lap
    Required columns are LapNumber, Position, LapStartTime
    Returns a sorted df by LapNumber then Position
    
    Args: input_df (pandas.core.frame.DataFrame)

    Returns: pandas.core.frame.DataFrame: input_df sorted by 'LapNumber' and 'Position' with an additional 'GapInSeconds' column
    '''
    #Empty gaps list
    gaps = []
    #Sort dataset so that we can iterate and directly identify drivers in front
    sorted_input_df = input_df.sort_values(['LapNumber','Position'])
    #iterate through dataset
    for row in range(0,sorted_input_df.shape[0],1):
        #create specific lap object
        lap = sorted_input_df.iloc[row]
        #check position existance
        if lap.Position:
            #avoid using lap 1, for obvious reasons
            if lap.LapNumber!=1:
                #skip position 1, their gap is always 0.000
                if lap.Position!=1:
                    print('\n\n',lap.LapNumber)
                    print(lap.LapStartTime,'laptime',lap.Driver,lap.LapNumber,'#')
                    print(sorted_input_df.iloc[row-1]['LapStartTime'],'previous laptime',sorted_input_df.iloc[row-1]['Driver'],sorted_input_df.iloc[row-1]['LapNumber'])
                    gap_timedelta = lap.LapStartTime - sorted_input_df.iloc[row-1]['LapStartTime']
                    print(gap_timedelta)
                    gap_seconds = gap_timedelta.total_seconds()
                    print(gap_seconds)
                    gaps.append(gap_seconds)
                else:
                    #add gap for position 1
                    print('adding gap 0 for first position')
                    gaps.append(float(0.000))
            else:
                print('lap 1 is skipped')
                gaps.append(float(0.000))
        else:
            print('position not found')
            gaps.append(np.NaN)
    sorted_input_df['GapInSeconds'] = gaps
    return sorted_input_df

def get_ideal_lap(driver,input_df):
    '''
    Required columns: Driver, DriverNumber, Team, S1InSeconds, S2InSeconds, S3InSeconds, LapTimeInSeconds

    Args: 
        driver (str)
        input_df (pandas.core.frame.DataFrame)

    Returns: Dict of best sector performances along with the ideal lap (sum of best sector times in seconds) for the 'driver'
    '''
    df = input_df[input_df['Driver']==driver]

    best_s1 = df['S1InSeconds'].min()
    best_s2 = df['S2InSeconds'].min()
    best_s3 = df['S3InSeconds'].min()
    best_lap = df['LapTimeInSeconds'].min()
    ideal_lap = best_s1+best_s2+best_s3
    improvement_margin = round(ideal_lap-best_lap,3)
    
    driver_number = df['DriverNumber'].iloc[1]
    team = df['Team'].iloc[1]

    result = {'Driver':driver,'DriverNumber':driver_number,'Team':team,'BestS1':best_s1,'BestS2':best_s2,'BestS3':best_s3,'BestLap':best_lap,'IdealLap':ideal_lap,'ImprovementMargin':improvement_margin}
    return result

def generate_improv_df(input_df):
    '''
    Generates a df with the following columns:
    ['Driver','DriverNumber','Team','BestS1','BestS2','BestS3','BestLap','IdealLap','ImprovementMargin']
    Required columns: Driver, DriverNumber, Team, S1InSeconds, S2InSeconds, S3InSeconds, LapTimeInSeconds 

    Args:
        input_df (pandas.core.frame.DataFrame)
    
    Returns:
        pandas.core.frame.DataFrame
    '''
    i=0
    improv_df = pd.DataFrame(columns=['Driver','DriverNumber','Team','BestS1','BestS2','BestS3','BestLap','IdealLap','ImprovementMargin'])
    for driver in input_df['Driver'].unique():
        ideal = get_ideal_lap(driver,input_df)
        improv_df = pd.concat([improv_df,pd.DataFrame(ideal,columns=improv_df.columns,index=[i])])
        i+=1
    return improv_df

def ideal_lap_chart(input_df,n=9):
    '''
    Plots ideal vs best lap chart for top 'n' drivers.
    Required columns: Driver, BestLap, IdealLap
    '''
    topN = input_df.sort_values(by='BestLap',ascending=True).iloc[0:n+1]
    plt.figure(figsize=(12,10))
    sns.scatterplot(topN,x='BestLap',y='Driver',hue='Driver',palette=driver_colors,legend=False,s=100)
    sns.scatterplot(topN,x='IdealLap',y='Driver',hue='Driver',palette=driver_colors_2,legend=False,s=100)
    plt.xticks(np.arange(topN['IdealLap'].min(),topN['BestLap'].max(),0.1))
    plt.grid(axis='both')

def generate_times_in_seconds(input_df):
    '''
    Generate 4 additional columns calculating Lap Time and each sector's time in seconds
    Required columns: LapTime, Sector1Time, Sector2Time, Sector3Time
    '''
    input_df['LapTimeInSeconds'] = input_df['LapTime'].dt.total_seconds()
    input_df['S1InSeconds'] = input_df['Sector1Time'].dt.total_seconds()
    input_df['S2InSeconds'] = input_df['Sector2Time'].dt.total_seconds()
    input_df['S3InSeconds'] = input_df['Sector3Time'].dt.total_seconds()
    #input_df.drop(columns=['LapTime','Sector1Time','Sector2Time','Sector3Time'],axis=1,inplace=True)
    return input_df

def race_pace_chart(input_df):
    '''
    Plots race pace box plot per each driver in the grid
    Required columns: Driver, LapTimeInSeconds
    TO BE IMPROVED: Filter out pit laps
    '''
    new_df = input_df[input_df['TrackStatus']=='1']
    plt.figure(figsize=(15,8))
    sns.boxplot(data=new_df,x='Driver',y='LapTimeInSeconds',hue='Driver',palette=driver_colors)
    plt.legend(loc='upper right')
    plt.title('Race Pace per Driver')
    plt.ylabel('Lap Time [s]')
    plt.xlabel('Driver')

def race_pace_comparison_chart(input_df,drv1,drv2):
    '''
    Plots race pace comparison trendlines for two drivers
    Required columns: Driver, LapNumber, LapTimeInSeconds,PitLap
    TO BE IMPROVED: Caculate yticks dinamically
    '''
    if 'PitLap' in input_df.columns:
        input_df = input_df[(input_df['LapNumber']!=1.0)&(input_df['TrackStatus']=='1')&(input_df['PitLap']!=1)]
        plt.figure(figsize=(15,5))
        sns.lineplot(data=input_df[(input_df['Driver']==drv1)|(input_df['Driver']==drv2)],x='LapNumber',y='LapTimeInSeconds',hue='Driver',palette=driver_colors)
        plt.xticks(ticks=input_df['LapNumber'].unique())
        #plt.yticks(np.arange(input_df['LapTimeInSeconds'].min()-0.5,input_df['LapTimeInSeconds'].max()+0.5,0.5))
        plt.title(f'Pace comparison {drv1} vs {drv2}')
        plt.ylabel('Lap Time [s]')
        plt.xlabel('Lap')
        plt.grid(color='grey')
    else:
        print('PitLap column missing, use utilities.one_hot_pit_laps')

def top_speed_comparison_chart(input_df):
    '''
    Plots top speed comparison
    Required columns: Driver, SpeedST
    TO BE IMPROVED: DYNAMICS LIM AND TICKS, PROBABLY BASED ON MIN AND MAX SPEED OF ALL DRIVERS' TOP SPEED (AND NOT ALL SPEEDS, AS THERE ARE OUTLIERS)
    '''
    plt.figure(figsize=(18,10))
    sns.barplot(data=input_df.groupby('Driver')['SpeedST'].max().sort_values(ascending=False),palette=driver_colors)
    plt.ylim(310,input_df['SpeedST'].max()+3)
    plt.yticks(np.arange(310,input_df['SpeedST'].max()+3,2),)
    plt.title('Max Speed Comparison per Driver')
    plt.ylabel('Max Speed at longest straight [km/h]')
    plt.xlabel('Driver')
    plt.grid(color='grey')

def position_switches_chart(input_df):
    '''
    Plots position changes during the race
    Required columns: LapNumber, Position, Driver
    TO BE IMPROVED: Add top_n parameter based on final position
    '''
    plt.figure(figsize=(30,10))
    sns.lineplot(data=input_df,x='LapNumber',y='Position',hue='Driver',palette=driver_colors)
    plt.yticks(np.arange(1,21,1))
    plt.xticks(np.arange(1,(input_df['LapNumber'].max()+1),1))
    plt.xlim(1,(input_df['LapNumber'].max()+2))
    plt.gca().invert_yaxis()
    plt.legend(loc='upper right')
    plt.grid(color='grey')

def delta_from_pole_chart(input_df):
    #Find fastest lap per driver
    fastest_laps = []
    for driver in input_df['Driver'].unique():
        fastest_lap_dr = input_df.pick_drivers(driver).pick_fastest()
        fastest_laps.append(fastest_lap_dr)
    #Get the laps object per each fastest lap
    from fastf1.core import Laps
    fastest_laps = Laps(fastest_laps)
    #Get pole lap
    pole_lap = fastest_laps.pick_fastest()
    #Generate delta
    fastest_laps['LapTimeDeltaInSeconds'] = (fastest_laps['LapTime'] - pole_lap['LapTime']).dt.total_seconds()
    #Sort df
    fastest_laps.sort_values('LapTimeDeltaInSeconds',inplace=True)
    fastest_laps.reset_index(inplace=True)
    fastest_laps.drop(columns=['index'],inplace=True)
    #Plot chart
    plt.figure(figsize=(15,8))
    ax = sns.barplot(orient='horizontal',data=fastest_laps.head(10),x='LapTimeDeltaInSeconds',y='Driver',hue='Driver',palette=driver_colors)
    plt.title('Delta from Pole Position - Shootout Qualifying')
    plt.ylabel('Driver')
    plt.xlabel('Delta [s]')
    plt.xticks(np.arange(fastest_laps['LapTimeDeltaInSeconds'].min(),fastest_laps['LapTimeDeltaInSeconds'].max(),0.1))
    custom_y_ticks_labels = [f'{team} {drv}' for team, drv, in zip(fastest_laps['Team'],fastest_laps['Driver'])]
    ax.set_yticklabels(custom_y_ticks_labels)
    plt.grid(axis='both',color='grey')
    plt.xlim(0.0,1.0)

def one_hot_pit_laps(input_df):
    '''
    Returns a new column called "PitLap" with value 1 if during that lap there has been a pit (either getting in or going out of the pitlane), else 0.
    Required columns: PitInTime, PitOutTime
    '''
    input_df['PitLap'] = ((input_df['PitInTime'].dt.total_seconds()>0) | (input_df['PitOutTime'].dt.total_seconds()>0)).astype(int)
    return input_df

def compare_stint_lap_times(input_df,drv,fuel_coeff=0.06):
    '''
    Returns df and chart with comparison of lap times between stints for a given driver
    Accepts a fuel_coefficient drag that adds incrementally to each lap time to take into account fuel tank weight reduction
        Default: 0.06s
    Required columns: Driver, LapNumber, PitLap, LapTimeInSeconds
    TO BE CORRECTED: PLOT SHOULD BE STINT-BASED, BUT YOU SHOULD HAVE THE INFO OF THE COMPOUND SOMEHOW
    '''
    df = input_df[((input_df['Driver']==drv) & (input_df['LapNumber']!=1))]
    df = df[df['PitLap']==0]
    df['FuelCorrectedLapTime'] = df['LapTimeInSeconds']+(df['LapNumber']-1)*fuel_coeff
    fig = sns.lineplot(data=df,x='LapNumber',y='FuelCorrectedLapTime',hue='Stint')
    plt.title(drv)
    return df,fig