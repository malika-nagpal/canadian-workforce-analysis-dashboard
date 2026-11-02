# Canadian Workforce Analysis Dashboard

An interactive data analytics project exploring workforce distribution, gender employment patterns, and engineering talent across Canada's provinces and territories.

Built using Python, Pandas, Dash, and Plotly, this dashboard transforms workforce datasets into interactive visualizations to support geographic comparisons and workforce exploration.

## Project Overview

The dashboard includes four interactive analyses:

### 1. Essential Services Distribution
- Explore the distribution of nurses, police officers, and firefighters across provinces and territories.
- Switch between raw workforce counts and population-normalized comparisons per 100,000 people.
- Compare workforce distribution across different regions.

### 2. Gender Employment by NOC Category
- Explore reported employment for men and women across different National Occupational Classification (NOC) major groups.
- Filter by province or territory and occupational category.
- Visualize employment distribution and compare the women-to-men employment ratio.

### 3. EV Factory Workforce Suitability
- Compare regional workforce availability across selected engineering disciplines:
  - Computer engineering
  - Electrical, electronics and communications engineering
  - Mechanical engineering
- Adjust the minimum workforce threshold.
- Identify regions that meet the selected workforce-size criterion.

This analysis is intended as an initial workforce screening exercise, not a comprehensive assessment of industrial site suitability.

### 4. Engineering Talent Heatmap
- Explore engineering workforce distribution across provinces and territories.
- Compare six engineering disciplines.
- Switch between absolute workforce counts and per-100,000 population views.

## Technologies Used

- **Python** — data processing and application logic
- **Pandas** — data manipulation and cleaning
- **NumPy** — numerical operations
- **Plotly** — interactive data visualizations
- **Dash** — interactive dashboard development
- **Jupyter Notebook** — exploratory analysis

## Repository Structure

```text
canadian-workforce-analysis-dashboard/
│
├── app.py
├── assets/
│   └── style.css
├── data/
│   ├── essential_services.csv
│   ├── data_gender_employment.csv
│   └── data_engineering.csv
├── notebooks/
│   └── canadian_workforce_analysis.ipynb
├── screenshots/
├── requirements.txt
└── README.md
```

## Running the Dashboard Locally

1. Clone the repository:

```bash
git clone https://github.com/malika-nagpal/canadian-workforce-analysis-dashboard.git
```

2. Navigate to the project directory:

```bash
cd canadian-workforce-analysis-dashboard
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Run the dashboard:

```bash
python app.py
```

6. Open the local address in your browser:

```text
http://127.0.0.1:8050/
```

## Data and Interpretation Notes

The project uses three CSV datasets covering essential services, gender employment, and engineering occupations.

The population denominators used in the per-capita calculations are retained from the original project notebook. The original project archive did not include complete data-source citations, dataset release dates, or a reference year for these population figures.

These values should therefore be independently verified before interpreting the per-capita results as official or current statistics.

## About

**Malika Nagpal**  
Honours Bachelor of Science in Data Science  
Wilfrid Laurier University

[LinkedIn](https://www.linkedin.com/in/malika-nagpal/)

[GitHub](https://github.com/malika-nagpal)
