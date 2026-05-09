# Data Sources & Citation Links

All datasets used in `finalproject.py` are derived from real, public, citable sources.
This document provides direct URLs for verification.

## Primary U.S. cancer surveillance

- **SEER (Surveillance, Epidemiology, and End Results) Program** — National Cancer Institute. Used for `historical_crc_trends.csv` (1975–2023 incidence and mortality rates by age group) and `seer_survival_by_stage.csv` (5-year relative survival).
  - Landing page: https://seer.cancer.gov/
  - Colorectal cancer fact sheet: https://seer.cancer.gov/statfacts/html/colorect.html
  - Explorer (rate trends): https://seer.cancer.gov/explorer/

- **CDC United States Cancer Statistics (USCS)** — joint CDC + NCI. Used for `state_crc_rates_real.csv` (state-level age-adjusted CRC rates per 100K with race, age, and sex breakdowns).
  - Landing page: https://www.cdc.gov/united-states-cancer-statistics/
  - Data Visualizations tool: https://www.cdc.gov/united-states-cancer-statistics/dataviz/index.html

- **American Cancer Society (ACS) — Cancer Facts & Figures (annual)**. Used for `cancer_totals_yearly.csv` (total U.S. new cancer cases and CRC cases per year, 2000–2024) and `colorectal_only_combined.csv` (state-level annual counts).
  - Landing page: https://www.cancer.org/research/cancer-facts-statistics/all-cancer-facts-figures.html
  - Cancer Statistics Center: https://cancerstatisticscenter.cancer.org/

## International cancer surveillance

- **IARC GLOBOCAN (Global Cancer Observatory)** — International Agency for Research on Cancer / WHO. Used for `globocan_2022_crc.csv` and `globocan_historical.csv` (country-level age-standardized incidence and mortality rates per 100K, GLOBOCAN editions 2012, 2018, 2022).
  - Landing page: https://gco.iarc.fr/
  - "Today" interactive (current rates): https://gco.iarc.fr/today
  - Historical editions archive: https://gco.iarc.fr/

## Risk factor evidence

- **World Cancer Research Fund / American Institute for Cancer Research (WCRF/AICR) Continuous Update Project, 2018**. Used for `crc_risk_factors_real.csv` (relative risks with 95% CIs for processed meat, red meat, alcohol, body fatness, height, physical activity, whole grains, fiber, dairy, calcium).
  - Colorectal Cancer Report: https://www.wcrf.org/diet-activity-and-cancer/cancer-types/colorectal-cancer/
  - Continuous Update Project: https://www.wcrf.org/research-policy/

- **IARC Monographs Vol. 100E** — smoking and CRC relative risk.
  - https://publications.iarc.who.int/Book-And-Report-Series/Iarc-Monographs-On-The-Identification-Of-Carcinogenic-Hazards-To-Humans/Personal-Habits-And-Indoor-Combustions-2012

- **Larsson SC et al. 2005** — diabetes and CRC risk (meta-analysis). Journal of the National Cancer Institute.
  - https://pubmed.ncbi.nlm.nih.gov/16288118/

## Behavioral risk factors

- **CDC Behavioral Risk Factor Surveillance System (BRFSS) 2022**. Used for `state_obesity_brfss.csv` (state adult obesity prevalence).
  - Landing page: https://www.cdc.gov/brfss/
  - Prevalence & trends data: https://www.cdc.gov/brfss/brfssprevalence/
  - Adult obesity prevalence maps: https://www.cdc.gov/obesity/data-and-statistics/adult-obesity-prevalence-maps.html

## Food and dietary data

- **FAO Food Balance Sheets (FAOSTAT)** — Food and Agriculture Organization of the United Nations. Used for `food_consumption_country.csv` (per-capita red meat, processed meat, fiber, fruit/vegetable consumption by country).
  - FAOSTAT Food Balances: https://www.fao.org/faostat/en/#data/FBS
  - Our World in Data mirror with visualizations: https://ourworldindata.org/meat-production

- **USDA Economic Research Service — Food Availability per Capita**. Used for `us_diet_trends.csv` (U.S. per-capita red meat, processed meat, added sugar over time).
  - https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/

- **Martínez Steele E et al. 2016 (NHANES ultra-processed food estimates)** — used for the ultra-processed % of calories series in `us_diet_trends.csv`.
  - BMJ Open: https://bmjopen.bmj.com/content/6/3/e009892

## Other supporting sources

- **U.S. Preventive Services Task Force (USPSTF) — 2021 colorectal cancer screening recommendation** (cited in narrative for the lowered screening age).
  - https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/colorectal-cancer-screening

- **Murphy CC et al. (2018) — Decrease in incidence of young-onset colorectal cancer before recent increase. Gastroenterology.**
  - https://pubmed.ncbi.nlm.nih.gov/30009816/

- **Siegel RL et al. — Cancer Statistics (annual ACS publication).**
  - https://acsjournals.onlinelibrary.wiley.com/journal/15424863

## Files generated for this dashboard

| File | Description |
|------|-------------|
| `historical_crc_trends.csv` | 1975–2023 yearly incidence/mortality, age-stratified |
| `cancer_totals_yearly.csv` | All-cancer vs CRC, 2000–2024 |
| `state_crc_rates_real.csv` | CDC state CRC rates per 100K with demographics |
| `state_obesity_brfss.csv` | State adult obesity prevalence (BRFSS 2022) |
| `globocan_2022_crc.csv` | Latest IARC country rates |
| `globocan_historical.csv` | IARC 2012, 2018, 2022 country comparison |
| `seer_survival_by_stage.csv` | SEER 5-year survival by stage |
| `crc_risk_factors_real.csv` | Published meta-analysis relative risks |
| `food_consumption_country.csv` | FAO per-capita food consumption by country |
| `us_diet_trends.csv` | USDA U.S. per-capita food trends 1970–2023 |

> All numeric values in the dashboard derive from these sources. Where rates were transcribed from agency reports, the `source` column in each CSV records the origin. Original raw downloads from each agency may be retrieved from the URLs above for replication.
