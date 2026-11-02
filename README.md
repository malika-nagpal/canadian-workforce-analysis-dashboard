# Canadian Workforce Analysis Dashboard

An interactive dashboard exploring Canadian workforce patterns across provinces and territories. The project uses Python, Pandas, Dash, and Plotly to turn tabular workforce data into interactive comparisons.

## Project overview

This project contains four dashboard views:

1. **Essential services distribution** — compare counts for nurses, police, and firefighters across provinces and territories, with raw-count and per-100,000 population views.
2. **Gender employment by NOC category** — compare reported employment for men and women by geography and National Occupational Classification (NOC) category.
3. **EV factory suitability analysis** — compare selected engineering disciplines across provinces and identify locations that meet a user-selected workforce threshold.
4. **Engineering talent heatmap** — explore engineering workforce counts by discipline and geography, with an absolute-count or per-capita view.

## Technology

- Python
- Pandas and NumPy
- Plotly Express and Graph Objects
- Dash
- Jupyter Notebook

## Repository structure

```text
canadian-workforce-analysis-dashboard/
├── app.py
├── data/
│   ├── data_engineering.csv
│   ├── data_gender_employment.csv
│   └── essential_services.csv
├── notebooks/
│   └── canadian_workforce_analysis.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Run locally

1. Clone or download this repository.
2. From the repository root, create and activate a virtual environment (recommended).
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   python app.py
   ```

5. Open the local address printed by Dash in your browser (typically `http://127.0.0.1:8050`).

The notebook version is available in `notebooks/`. The project video is linked from the notebook.

## Data files and interpretation notes

The `data/` directory contains the three CSV files supplied with the original project archive. The archive did not include source citations, dataset release dates, or a citation for the population denominators used in the per-capita calculations. Those details should be verified against the original course/project materials and added here before presenting the figures as official or current statistics.

The population values are retained from the original notebook to preserve the original analysis. Per-capita results therefore depend on those embedded population values and should be interpreted accordingly.

## Notes on the prepared version

The original analysis and dashboard interactions have been retained. Two packaging/runtime issues were addressed: the population DataFrame is consistently referenced as `df_population`, and the project-video URL is stored as a Markdown link rather than an executable Python code cell. The standalone `app.py` reads the CSVs from the repository's `data/` directory.

## Further improvements

- Add the original data-source citations and population reference year.
- Add verified dashboard screenshots.
- Add tests for data cleaning and per-capita calculations.

## Author

**Malika Nagpal** — Honours Bachelor of Science, Data Science, Wilfrid Laurier University (2026).

[LinkedIn](https://www.linkedin.com/in/malika-nagpal/)
