# F1 Data Analysis Project

## Overview

This project aims to analyze Formula 1 (F1) race data from various race weekends using the open-source **FastF1 API**. The goal is to download data from Free Practice, Qualifying, and Race sessions, perform exploratory data analysis (EDA), and create visualizations that help better understand driver performance, race strategies, and other key metrics.

The analysis is done using Python libraries such as Pandas, NumPy, Seaborn, and Matplotlib, and is organized in a reproducible workflow that allows the user to build on past analyses from previous weekends.

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

1. **Download Data**: You can download the race weekend data by using FastF1 API calls, which are integrated into the Jupyter notebooks.
2. **Run Analysis**: After loading the data, you can apply the standardized functions for each type of analysis you wish to perform (e.g., ideal lap comparisons, race pace comparisons, etc.).
3. **Apply Functions**: Each new analysis will use functions from `Utilities.py`. If any new analysis is added for a new weekend, that function will also be added to `Utilities.py`.
4. **Visualize**: Charts will be generated using Seaborn/Matplotlib to visualize key metrics, such as ideal lap comparisons, top speed, race pace, etc.

---

## Acknowledgments

- **FastF1 API**: For providing open-source data on F1 sessions.
- **Seaborn, Matplotlib, Pandas**: For enabling powerful data analysis and visualization.
