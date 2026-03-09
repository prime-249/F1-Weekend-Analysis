# F1 Data Analysis Project

## Overview

This project aims to analyze Formula 1 (F1) race data from various race weekends using the open-source **FastF1 API**. The goal is to download data from Free Practice, Qualifying, and Race sessions, perform exploratory data analysis (EDA), and create visualizations that help better understand driver performance, race strategies, and other key metrics.

The analysis is done using Python libraries such as Pandas, NumPy, Seaborn, and Matplotlib, and is organized in a reproducible workflow that allows the user to build on past analyses from previous weekends.

UPDATE 2026: All previously generated analysis and utilities have been stored in a new module called "Main.py". This module contains a Session class with all the information and analysis ready at-hand. All old data and functionalities have been maintained within a new folder called "2025".

---

## Tools & Libraries

- **Python 3.x**
- **Jupyter Notebook**
- **Pandas**
- **NumPy**
- **Seaborn**
- **Matplotlib**
- **FastF1 API**

---

## Workflow

1. **Download Data**: Data is downloaded from the FastF1 API for each race weekend (Free Practice, Qualifying, and Race sessions).
2. **Initial Analysis**: For each new weekend, data is analyzed for the first time using custom logic in Jupyter Notebooks.
3. **Standardize Functions**: Any new analysis or transformation logic is then standardized and added to the utility package `Utilities.py` as a reusable function.
4. **Subsequent Weekends**: For subsequent weekends, previously defined functions are applied to new data, and new functions are added as necessary.

---

## Features

- **Caching**: The FastF1 API caching feature is used to prevent overloading the servers and to speed up subsequent data retrievals.
- **Color Consistency**: A dictionary is used to map teams and drivers to their specific colors, ensuring consistent color schemes across all visualizations.
- **Reusable Functions**: Each analysis performed is standardized into reusable, well-documented functions that simplify future analyses.

---

## Usage

1. **Import Session from Main**: Import Session class from Main module. (from Main import Session)
2. **Initalize Session object**: Initialize a Session object passing year, location, and session name. E.g. my_session = Session('Australia', 'R', 2026)
3. **Access df or charts**: Either read data on your own calling the attribute df (my_session.df) or use the built-in functions to show charts and analysis.

---

## Acknowledgments

- **FastF1 API**: For providing open-source data on F1 sessions.
- **Seaborn, Matplotlib, Pandas, Numpy**: For enabling powerful data analysis and visualization.
