# Global Food Wastage Analysis — Pandas Edition

Companion Python/Pandas build of the project you already completed in Power BI. Same dataset, same project brief, executed end-to-end.

## Files in this delivery

| File | What it is |
|---|---|
| `Food_Waste_Analysis.ipynb` | Main Jupyter notebook — cleaning, EDA, all 4 required charts, forecasting, insights. Fully executed with outputs saved in. |
| `global_food_wastage_cleaned.csv` | Cleaned dataset (standardized column names, added `Continent` and `Industrial_Waste_Pct` columns) |
| `Food_Waste_Dashboard.html` | Standalone interactive dashboard — open in any browser, no install needed. Has a Country filter. |
| `dash_app.py` | Live Plotly Dash app with **all three filters** (Country, Year, Food Category) working independently. Run locally: `pip install dash pandas plotly` then `python dash_app.py`. |

## What was done, mapped to the brief

- **Data sourcing**: used the provided dataset (5,000 rows, 20 countries, 8 food categories, 2018–2024).
- **Cleaning**: checked/handled missing values and duplicates (none found), standardized column names, added a `Continent` field since the raw data only has `Country` (no region column existed), added `Industrial_Waste_Pct` as the complement of `Household_Waste_Pct`.
- **EDA**: waste by region/food type/year, top countries, year-over-year change (used as the "seasonal/growth" analysis since the data is annual, not monthly), economic loss and household waste share by region.
- **Visuals**: line chart (2018–2024 trend), bar charts (by continent and by country), choropleth map (economic loss by country), pie chart (household vs. industrial split).
- **Predictive analysis**: Linear Regression forecast for 2026 total waste and estimated dollar cost. ARIMA was considered but skipped — 7 annual points is too short a series to fit reliably, so this is flagged in the notebook as a limitation rather than silently using an unreliable model.
- **Dashboard**: static HTML (portable, one filter) + Dash script (full 3-filter version, needs to be run locally).

## Headline numbers (from this run)

- **Top waste-generating countries**: Turkey, Canada, Spain (all ~6.8M tons over 2018–2024, tightly clustered — not one dominant outlier)
- **By continent**: Asia (43.3M tons) and Europe (37.7M tons) lead, well ahead of North America (19.8M)
- **Trend**: total waste hovered around 17–18.4M tons/year with no strong upward or downward trend — 2023 was the peak year
- **Household waste share**: averages ~50% globally, meaning consumer-level waste and industrial/supply-chain waste are roughly equal contributors
- **2026 forecast**: see the notebook's Predictive Analysis section for the exact projected tonnage and dollar figure — it updates automatically if you re-run with new data

## Note on the dashboard filters

The brief asks for a dashboard with country, year, and food-type filters. A single static HTML file can't cleanly support three independent, freely-combinable dropdowns without a backend (the combinatorics get unwieldy). So:
- `Food_Waste_Dashboard.html` — works anywhere, filters by **Country**
- `dash_app.py` — the true multi-filter version; run it locally for the full Country + Year + Food Category experience described in the brief
