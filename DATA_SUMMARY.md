# Dataset Summary
This document lists every dataset powering the Colorectal Cancer Disparities Dashboard, including row count, column count, column list, source, and a 5-row snippet for each.

## Inventory at a glance

- **11 datasets** total
- **1,339 rows combined**
- **76 columns combined**

| File | Rows | Columns | Source |
|------|------:|--------:|--------|
| `historical_crc_trends.csv` | 22 | 5 | SEER 9 Registry / ACS Cancer Statistics 2023 |
| `cancer_totals_yearly.csv` | 15 | 8 | ACS Cancer Facts & Figures (annual editions) |
| `state_crc_rates_real.csv` | 51 | 17 | CDC State Cancer Statistics |
| `state_obesity_brfss.csv` | 51 | 3 | CDC BRFSS 2022 |
| `globocan_2022_crc.csv` | 27 | 6 | IARC GLOBOCAN 2022 |
| `globocan_historical.csv` | 60 | 6 | IARC GLOBOCAN 2012 / 2018 / 2022 |
| `seer_survival_by_stage.csv` | 4 | 4 | SEER 2014–2020 |
| `crc_risk_factors_real.csv` | 12 | 8 | WCRF/AICR 2018; IARC Monograph Vol. 100E; Larsson 2005 |
| `food_consumption_country.csv` | 27 | 6 | FAO Food Balance Sheets 2020 |
| `us_diet_trends.csv` | 12 | 6 | USDA ERS Food Availability + NHANES (Martínez Steele 2016) |
| `colorectal_only_combined.csv` | 1,058 | 7 | ACS Cancer Facts & Figures (state-level extracts) |

---

## `historical_crc_trends.csv`

- **Rows:** 22
- **Columns:** 5
- **Source:** SEER 9 Registry / ACS Cancer Statistics 2023
- **URL:** https://seer.cancer.gov/statfacts/html/colorect.html
- **Description:** 1975–2023 yearly CRC incidence and mortality rates per 100K, stratified by age group (<50 vs 50+).
- **Column list:** `year`, `age_group`, `incidence_rate`, `mortality_rate`, `source`

**Snippet (first 5 rows):**

| year | age_group | incidence_rate | mortality_rate | source |
|---|---|---|---|---|
| 1,975 | <50 | 5.90 | 1.80 | SEER 9 / ACS Cancer Statistics |
| 1,980 | <50 | 6.10 | 1.90 | SEER 9 / ACS Cancer Statistics |
| 1,985 | <50 | 6.20 | 1.90 | SEER 9 / ACS Cancer Statistics |
| 1,990 | <50 | 6.70 | 2.00 | SEER 9 / ACS Cancer Statistics |
| 1,995 | <50 | 7.20 | 2.20 | SEER 9 / ACS Cancer Statistics |

---

## `cancer_totals_yearly.csv`

- **Rows:** 15
- **Columns:** 8
- **Source:** ACS Cancer Facts & Figures (annual editions)
- **URL:** https://www.cancer.org/research/cancer-facts-statistics/all-cancer-facts-figures.html
- **Description:** Total U.S. new cancer cases vs CRC cases per year (2000–2024) with CRC share %.
- **Column list:** `year`, `total_new_cancer_cases`, `crc_cases`, `crc_pct_of_total`, `total_cancer_deaths`, `crc_deaths`, `crc_death_pct`, `source`

**Snippet (first 5 rows):**

| year | total_new_cancer_cases | crc_cases | crc_pct_of_total | total_cancer_deaths | crc_deaths | crc_death_pct | source |
|---|---|---|---|---|---|---|---|
| 2,000 | 1,220,100 | 130,200 | 10.70 | 552,200 | 56,300 | 10.20 | ACS Cancer Facts & Figures |
| 2,005 | 1,372,910 | 145,290 | 10.60 | 570,280 | 56,290 | 9.90 | ACS Cancer Facts & Figures |
| 2,010 | 1,529,560 | 142,570 | 9.30 | 569,490 | 51,370 | 9.00 | ACS Cancer Facts & Figures |
| 2,012 | 1,638,910 | 143,460 | 8.80 | 577,190 | 51,690 | 9.00 | ACS Cancer Facts & Figures |
| 2,014 | 1,665,540 | 136,830 | 8.20 | 585,720 | 50,310 | 8.60 | ACS Cancer Facts & Figures |

---

## `state_crc_rates_real.csv`

- **Rows:** 51
- **Columns:** 17
- **Source:** CDC State Cancer Statistics
- **URL:** https://www.cdc.gov/united-states-cancer-statistics/dataviz/index.html
- **Description:** Age-adjusted CRC rates per 100K with race, age, and sex breakdowns for all 50 states + DC.
- **Column list:** `state`, `population`, `crc_rate_total`, `crc_rate_female_18_44`, `crc_rate_male_18_44`, `crc_rate_female_45_64`, `crc_rate_male_45_64`, `crc_rate_female_65plus`, `crc_rate_male_65plus`, `crc_rate_white`, `crc_rate_black`, `crc_rate_asian`, `crc_rate_indigenous`, `crc_rate_hispanic`, `crc_rate_early_onset`, `crc_rate_traditional`, `disparity_ratio_black_white`

**Snippet (first 5 rows):**

| state | population | crc_rate_total | crc_rate_female_18_44 | crc_rate_male_18_44 | crc_rate_female_45_64 | crc_rate_male_45_64 | crc_rate_female_65plus | crc_rate_male_65plus | crc_rate_white | crc_rate_black | crc_rate_asian | crc_rate_indigenous | crc_rate_hispanic | crc_rate_early_onset | crc_rate_traditional | disparity_ratio_black_white |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Alabama | 33,387,205.00 | 19.40 | 1.60 | 2.30 | 18.00 | 28.70 | 78.40 | 106.00 | 15.90 | 24.40 | 0.00 | 0.00 | 5.70 | 1.95 | 57.78 | 1.53 |
| Alaska | 4,966,180.00 | 11.90 | 0.00 | 0.00 | 15.30 | 17.60 | 71.70 | 102.30 | 13.60 | 0.00 | 12.50 | 34.70 | 0.00 | 0.00 | 51.73 | 0.00 |
| Arizona | 44,845,598.00 | 14.90 | 1.30 | 1.40 | 12.60 | 19.20 | 67.60 | 85.20 | 13.80 | 18.70 | 10.60 | 10.10 | 13.10 | 1.35 | 46.15 | 1.36 |
| Arkansas | 20,382,448.00 | 21.20 | 1.90 | 2.20 | 19.70 | 28.60 | 85.80 | 114.40 | 17.70 | 26.30 | 0.00 | 0.00 | 8.10 | 2.05 | 62.12 | 1.49 |
| California | 261,135,696.00 | 14.00 | 1.20 | 1.40 | 13.40 | 17.90 | 75.30 | 93.30 | 14.40 | 21.20 | 11.60 | 7.70 | 11.70 | 1.30 | 49.98 | 1.47 |

---

## `state_obesity_brfss.csv`

- **Rows:** 51
- **Columns:** 3
- **Source:** CDC BRFSS 2022
- **URL:** https://www.cdc.gov/brfss/brfssprevalence/
- **Description:** Adult obesity prevalence (%) by state.
- **Column list:** `state`, `obesity_pct_adults`, `source`

**Snippet (first 5 rows):**

| state | obesity_pct_adults | source |
|---|---|---|
| West Virginia | 41.00 | CDC BRFSS 2022 |
| Mississippi | 40.10 | CDC BRFSS 2022 |
| Louisiana | 39.90 | CDC BRFSS 2022 |
| Oklahoma | 39.40 | CDC BRFSS 2022 |
| Alabama | 39.20 | CDC BRFSS 2022 |

---

## `globocan_2022_crc.csv`

- **Rows:** 27
- **Columns:** 6
- **Source:** IARC GLOBOCAN 2022
- **URL:** https://gco.iarc.fr/today
- **Description:** Latest country-level CRC age-standardized incidence and mortality rates per 100K.
- **Column list:** `country`, `region`, `incidence_asr_per_100k`, `mortality_asr_per_100k`, `hdi_tier`, `source`

**Snippet (first 5 rows):**

| country | region | incidence_asr_per_100k | mortality_asr_per_100k | hdi_tier | source |
|---|---|---|---|---|---|
| Hungary | Europe | 41.10 | 18.70 | Very high | IARC GLOBOCAN 2022 |
| Slovakia | Europe | 39.30 | 17.50 | Very high | IARC GLOBOCAN 2022 |
| Norway | Europe | 38.50 | 11.00 | Very high | IARC GLOBOCAN 2022 |
| Netherlands | Europe | 37.50 | 11.70 | Very high | IARC GLOBOCAN 2022 |
| Denmark | Europe | 36.90 | 12.10 | Very high | IARC GLOBOCAN 2022 |

---

## `globocan_historical.csv`

- **Rows:** 60
- **Columns:** 6
- **Source:** IARC GLOBOCAN 2012 / 2018 / 2022
- **URL:** https://gco.iarc.fr/
- **Description:** Decade-long country CRC rate comparison across three GLOBOCAN editions.
- **Column list:** `country`, `region`, `edition_year`, `incidence_asr_per_100k`, `mortality_asr_per_100k`, `source`

**Snippet (first 5 rows):**

| country | region | edition_year | incidence_asr_per_100k | mortality_asr_per_100k | source |
|---|---|---|---|---|---|
| Hungary | Europe | 2,012 | 51.20 | 23.50 | IARC GLOBOCAN 2012 |
| Hungary | Europe | 2,018 | 47.30 | 20.70 | IARC GLOBOCAN 2018 |
| Hungary | Europe | 2,022 | 41.10 | 18.70 | IARC GLOBOCAN 2022 |
| Slovakia | Europe | 2,012 | 47.80 | 21.00 | IARC GLOBOCAN 2012 |
| Slovakia | Europe | 2,018 | 43.20 | 19.10 | IARC GLOBOCAN 2018 |

---

## `seer_survival_by_stage.csv`

- **Rows:** 4
- **Columns:** 4
- **Source:** SEER 2014–2020
- **URL:** https://seer.cancer.gov/statfacts/html/colorect.html
- **Description:** 5-year relative survival by stage at diagnosis.
- **Column list:** `stage`, `5_year_survival_rate`, `description`, `source`

**Snippet (first 5 rows):**

| stage | 5_year_survival_rate | description | source |
|---|---|---|---|
| Localized | 91.30 | Cancer confined to primary site | SEER 2014-2020 |
| Regional | 75.20 | Cancer spread to regional lymph nodes | SEER 2014-2020 |
| Distant | 16.90 | Cancer has metastasized | SEER 2014-2020 |
| All Stages Combined | 65.00 | Overall 5-year relative survival | SEER 2014-2020 |

---

## `crc_risk_factors_real.csv`

- **Rows:** 12
- **Columns:** 8
- **Source:** WCRF/AICR 2018; IARC Monograph Vol. 100E; Larsson 2005
- **URL:** https://www.wcrf.org/diet-activity-and-cancer/cancer-types/colorectal-cancer/
- **Description:** Published meta-analysis relative risks (RR) with 95% CIs for modifiable factors.
- **Column list:** `risk_factor`, `direction`, `relative_risk`, `ci_lower`, `ci_upper`, `exposure_unit`, `evidence_grade`, `source`

**Snippet (first 5 rows):**

| risk_factor | direction | relative_risk | ci_lower | ci_upper | exposure_unit | evidence_grade | source |
|---|---|---|---|---|---|---|---|
| Processed meat | Increases | 1.18 | 1.10 | 1.28 | per 50g/day | Convincing | WCRF/AICR 2018 |
| Red meat | Increases | 1.12 | 1.04 | 1.21 | per 100g/day | Probable | WCRF/AICR 2018 |
| Alcohol consumption | Increases | 1.07 | 1.05 | 1.10 | per 10g/day ethanol | Convincing | WCRF/AICR 2018 |
| Body fatness (BMI) | Increases | 1.05 | 1.03 | 1.07 | per 5 kg/m2 | Convincing | WCRF/AICR 2018 |
| Adult attained height | Increases | 1.04 | 1.02 | 1.06 | per 5cm | Convincing | WCRF/AICR 2018 |

---

## `food_consumption_country.csv`

- **Rows:** 27
- **Columns:** 6
- **Source:** FAO Food Balance Sheets 2020
- **URL:** https://www.fao.org/faostat/en/#data/FBS
- **Description:** Per-capita country red meat, processed meat, fiber, fruit/vegetable consumption.
- **Column list:** `country`, `red_meat_kg_per_capita_yr`, `processed_meat_kg_per_capita_yr`, `fiber_g_per_capita_day`, `fruit_veg_kg_per_capita_yr`, `source`

**Snippet (first 5 rows):**

| country | red_meat_kg_per_capita_yr | processed_meat_kg_per_capita_yr | fiber_g_per_capita_day | fruit_veg_kg_per_capita_yr | source |
|---|---|---|---|---|---|
| Argentina | 49.70 | 11.00 | 18.50 | 140 | FAO Food Balance Sheets 2020 |
| USA | 37.00 | 17.00 | 16.00 | 200 | FAO/USDA ERS 2020 |
| Australia | 38.50 | 15.00 | 17.50 | 180 | FAO 2020 |
| Brazil | 33.00 | 8.00 | 19.00 | 150 | FAO 2020 |
| France | 35.00 | 15.00 | 21.00 | 180 | FAO 2020 |

---

## `us_diet_trends.csv`

- **Rows:** 12
- **Columns:** 6
- **Source:** USDA ERS Food Availability + NHANES (Martínez Steele 2016)
- **URL:** https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/
- **Description:** U.S. per-capita red meat, processed meat, sugar, ultra-processed % over time, 1970–2023.
- **Column list:** `year`, `red_meat_lbs_per_capita`, `processed_meat_lbs_per_capita`, `sugar_added_lbs_per_capita`, `ultraprocessed_pct_calories`, `source`

**Snippet (first 5 rows):**

| year | red_meat_lbs_per_capita | processed_meat_lbs_per_capita | sugar_added_lbs_per_capita | ultraprocessed_pct_calories | source |
|---|---|---|---|---|---|
| 1,970 | 131.70 | 15.50 | 119.10 | 53.50 | USDA ERS / NHANES estimates |
| 1,975 | 128.30 | 15.80 | 118.10 | 54.00 | USDA ERS / NHANES estimates |
| 1,980 | 126.40 | 16.00 | 120.10 | 55.50 | USDA ERS / NHANES estimates |
| 1,985 | 124.10 | 16.50 | 127.40 | 56.50 | USDA ERS / NHANES estimates |
| 1,990 | 112.30 | 17.00 | 132.50 | 57.50 | USDA ERS / NHANES estimates |

---

## `colorectal_only_combined.csv`

- **Rows:** 1,058
- **Columns:** 7
- **Source:** ACS Cancer Facts & Figures (state-level extracts)
- **URL:** https://www.cancer.org/research/cancer-facts-statistics/all-cancer-facts-figures.html
- **Description:** Annual state-level CRC case and death counts (raw counts).
- **Column list:** `year`, `geography_level`, `state`, `cancer_type`, `sex`, `metric`, `value`

**Snippet (first 5 rows):**

| year | geography_level | state | cancer_type | sex | metric | value |
|---|---|---|---|---|---|---|
| 2,015 | state | Alabama | colon_rectum | All | cases | 2,150 |
| 2,015 | state | Alabama | colon_rectum | All | deaths | 930 |
| 2,015 | state | Alaska | colon_rectum | All | cases | 290 |
| 2,015 | state | Alaska | colon_rectum | All | deaths | 90 |
| 2,015 | state | Arizona | colon_rectum | All | cases | 2,440 |

---

