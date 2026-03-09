################ Libraries
import pandas as pd
import numpy as np
import fastf1
import os
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import seaborn as sns

################ Utilities
team_colors = {
    "McLaren": "#FF8700",
    "Mercedes": "#00B2A9",
    "Ferrari": "#821729",
    "Red Bull Racing": "#003773",
    "Aston Martin": "#037A68",
    "Alpine": "#F282B4",
    "Williams": "#00A0DE",
    "Haas": "#EB0A1E",
    "Audi": "#00E701",
    "Racing Bulls": "#FFFFFF",
    "Cadillac": "#001A44",
}

driver_colors = {
    # McLaren
    "NOR": "#FF9800",
    "PIA": "#FFB766",

    # Mercedes
    "RUS": "#00D2BE",
    "ANT": "#39E0C6",

    # Ferrari
    "LEC": "#9B1B30",
    "HAM": "#C81D37",

    # Red Bull Racing
    "VER": "#002D5A",
    "HAD": "#1A4E8A",

    # Aston Martin
    "ALO": "#028061",
    "STR": "#03A678",

    # Alpine
    "GAS": "#FF66A1",
    "COL": "#D94A90",

    # Williams
    "ALB": "#0096C9",
    "SAI": "#00B6F1",

    # Haas
    "OCO": "#D91A26",
    "BEA": "#F52439",

    # Audi
    "HUL": "#4EF535",
    "BOR": "#26D401",

    # Racing Bulls
    "LAW": "#F2F2F2",
    "LIN": "#DDD5D5",

    # Cadillac
    "BOT": "#002868",
    "PER": "#0047AB",
}

compound_colors = {
    'SOFT':'#FF0000',
    'MEDIUM':'#FFFF00',
    'HARD':'#808080'
}

################ Constructor
class Session:
    """
    Represents a fastf1 session. It holds information such as the session's type (Qualy, Race, usually), year, and location
    Generates a pandas dataframe with the "laps" attribute of the session, cleans it, and generates various analyses.
    """
    def __init__(self, grand_prix:str, session:str, year:int):
        """
        Initialize a session object.

        Args:
            - grand_prix (str): The GP location or name. E.g. 'Australia', 'Monaco', or 'Belgium'.
            - session (str): The session of the weekend. E.g. 'Q', 'R', 'FP1'.
            - year (int): The year in which the session has been held.

            See fastf1 documentation for more info: https://docs.fastf1.dev/api_reference/index.html (All rights reserved, do not use this code for commercial purposes.)
        """
        self.grand_prix = grand_prix
        self.session = session
        self.year = year

        self._generate_cache()
        self._load_data()
        self._convert_times_in_seconds()
        
        if self.session == 'R':
            self._one_hot_pit_laps()
    
    def _load_data(self):
        """
        Loads the data and stores the laps dataset in the attribute "df" of the Session instance.
        """
        print('-'*15,'Polling and loading session data...')
        sess = fastf1.get_session(self.year, self.grand_prix, self.session)
        sess.load()
        print('-'*15,'Extracting laps dataset...')
        self.df = sess.laps
        
        print('-'*15,'Dataset stored.')
    
    def _generate_cache(self):
        """
        Generates the cache folder (for obvious reasons) in the same directory the Session instance is initialized
        """
        cache_folder = 'cache_folder' #Name of the file
        print('-'*15,'Deciding where to store cache...')
        if not os.path.exists(cache_folder):
            print('-'*15,'Cache folder not found.')
            os.makedirs(cache_folder)
            print('-'*15,'Cache folder generated.')
        fastf1.Cache.enable_cache(cache_folder)
        print('-'*15,'Cache folder identified.')

    def _convert_times_in_seconds(self):
        """
        Converts all time-based columns in seconds-based columns for better usage.
        Drops the already existing columns.
        """

        self.df['LapTime'] = self.df['LapTime'].dt.total_seconds()
        self.df['Sector1Time'] = self.df['Sector1Time'].dt.total_seconds()
        self.df['Sector2Time'] = self.df['Sector2Time'].dt.total_seconds()
        self.df['Sector3Time'] = self.df['Sector3Time'].dt.total_seconds()
    
    def _one_hot_pit_laps(self):
        """
        Generates new column called "PitLap" with value 1 for laps where the driver has pitted.
        """
        self.df['PitLap'] = ((self.df['PitInTime'].dt.total_seconds()>0) | (self.df['PitOutTime'].dt.total_seconds()>0)).astype(int)

    def chart_race_pace(self):
        """
        Generates a box plot chart for each driver's race pace during green-flag laps. Pitting laps are still considered.
        Drivers are ordered by median lap time.

        """
        if self.session != 'R':
            raise TypeError('Please load a race session for this functionality.')
        else:
            print('-'*15,'Generating Race Pace chart...')
            pass
    
        masked_df = self.df[self.df['TrackStatus'] == '1']

        valid_races = []
        for d in masked_df.groupby('Driver')['LapTime'].count().reset_index().itertuples():
            if d.LapTime > 10:
                valid_races.append(d.Driver)
        
        masked_df = masked_df[masked_df['Driver'].isin(valid_races)]

        fig, ax = plt.subplots(figsize=(15, 8))

        driver_order = (
            masked_df.groupby("Driver")["LapTime"]
            .median()
            .sort_values()
            .index
        )

        sns.boxplot(
            data=masked_df,
            x='Driver',
            y='LapTime',
            hue='Driver',
            palette=driver_colors,
            ax=ax,
            order=driver_order
        )

        ax.legend(loc='upper right')
        ax.set_title('Race Pace per Driver')
        ax.set_ylabel('Lap Time [s]')
        ax.set_xlabel('Driver')

        self.race_pace_chart = fig
        print('-'*15, 'Race Pace chart generated.')
        
    def chart_race_pace_comparison(self, drivers: tuple):
        """
        Generates a race pace comparison chart between two drivers.
        Only green-flag laps will be stored, while each driver's pitting lap(s) will be skipped for that driver only.

        Args:
            drivers (tuple): Tuple containing the two driver aliases, e.g. ('RUS','LEC')
        """
        drv1, drv2 = drivers
        available_drivers = self.df['Driver'].unique()

        if (drv1 not in available_drivers) | (drv2 not in available_drivers):
            raise ValueError(f'Missing driver. The drivers you entered are: {drv1}, {drv2}. Choose among this list: \n{available_drivers}')
        else:
            print('-'*15,'Generating race pace comparison between',drivers)
            pass

        filtered_df = self.df[
            (self.df['LapNumber'] != 1.0) &
            (self.df['TrackStatus'] == '1') &
            (self.df['PitLap'] != 1)
        ]

        fig, ax = plt.subplots(figsize=(15, 5))

        sns.lineplot(
            data=filtered_df[(filtered_df['Driver'] == drv1) | (filtered_df['Driver'] == drv2)],
            x='LapNumber',
            y='LapTime',
            hue='Driver',
            palette=driver_colors,
            ax=ax
        )

        ax.set_xticks(filtered_df['LapNumber'].unique())

        ax.set_title(f'Pace Comparison: {drv1} vs {drv2}')
        ax.set_ylabel('Lap Time [s]')
        ax.set_xlabel('Lap')
        ax.grid(color='grey')

        self.pace_comparison_chart = fig

    def chart_top_speed_comparison(self):
        """
        Generates top speed comparison chart between all drivers
        """
        fig, ax = plt.subplots(figsize=(18,10))
        min_maximum_speed = (self.df.groupby('Driver')['SpeedST'].max()).min()
        max_maximum_speed = (self.df.groupby('Driver')['SpeedST'].max()).max()
        sns.barplot(data=self.df.groupby('Driver')['SpeedST'].max().sort_values(ascending=False),
                    palette=driver_colors
                )
        ax.set_ylim(min_maximum_speed,max_maximum_speed+3)
        ax.set_yticks(np.arange(min_maximum_speed,max_maximum_speed+3,2),)
        ax.set_title('Max Speed Comparison per Driver')
        ax.set_ylabel('Max Speed at longest straight [km/h]')
        ax.set_xlabel('Driver')
        ax.grid(color='grey')

        self.top_speed_chart = fig
        print('-'*15, 'Top speed comparison chart generated.')