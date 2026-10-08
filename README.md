# CMS Hospital Readmission Performance Dashboard

## Project Overview

This project is an interactive Streamlit dashboard that analyzes hospital readmission performance using data from the Centers for Medicare & Medicaid Services (CMS) Hospital Readmissions Reduction Program.

The dashboard allows users to compare hospitals, states, and medical-condition measures using Excess Readmission Ratios, expected readmission rates, and predicted readmission rates.

## Business Problem

Hospitals need to monitor readmission performance and identify areas that may require quality-improvement attention. An Excess Readmission Ratio above 1.00 indicates that readmissions were higher than expected relative to the CMS comparison standard.

This dashboard helps users identify hospitals, states, and medical-condition measures that may require additional performance review.

## Intended Users

The intended users of this application include:

- Hospital administrators
- Quality-improvement managers
- Healthcare operations managers
- Case-management teams
- Healthcare data analysts

## Questions the App Helps Answer

The dashboard helps users answer the following questions:

1. Which hospitals have the highest average Excess Readmission Ratios?
2. Which states have the highest average Excess Readmission Ratios?
3. How does readmission performance vary by medical-condition measure?
4. How does predicted readmission compare with expected readmission?
5. Which hospitals or medical conditions may require additional quality-improvement review?

## Application Features

The Streamlit application includes:

- Hospital or state ranking selection
- Medical-condition filters
- State filters
- Slider to select the number of hospitals or states displayed
- Interactive hospital and state ranking chart
- Average readmission ratio chart by medical condition
- Predicted versus expected readmission-rate scatterplot
- Performance classification based on the Excess Readmission Ratio
- Summary metrics and chart interpretation guidance
- Hover information for hospital, state, condition, and readmission performance

## Visualizations

### 1. Hospital and State Ranking

This interactive horizontal bar chart ranks hospitals or states by their average Excess Readmission Ratio.

The chart includes:

- **X-axis:** Average Excess Readmission Ratio
- **Y-axis:** Hospital or state
- **Color:** Average Excess Readmission Ratio
- **Reference value:** Excess Readmission Ratio of 1.00

Values above 1.00 indicate readmissions were higher than expected relative to the CMS comparison standard.

### 2. Average Readmission Ratio by Medical Condition

This horizontal bar chart compares the average Excess Readmission Ratio across CMS medical-condition measures.

The chart includes:

- **X-axis:** Average Excess Readmission Ratio
- **Y-axis:** Medical condition
- **Reference line:** Ratio of 1.00

Medical conditions with ratios above 1.00 have higher average readmissions relative to the CMS expected level. A summary table displays the average ratio for each medical condition.

### 3. Predicted Versus Expected Readmission Rate

This interactive scatterplot compares predicted readmission rates with expected readmission rates.

The chart includes:

- **X-axis:** Expected Readmission Rate
- **Y-axis:** Predicted Readmission Rate
- **Color:** Performance classification
- **Green points:** At or below expected performance
- **Red points:** Above expected performance

Each point represents a hospital and medical-condition measure. Users can hover over the points to view the facility name, state, medical condition, Excess Readmission Ratio, expected readmission rate, and predicted readmission rate.

## Dataset

The dataset used in this project is the CMS FY 2026 Hospital Readmissions Reduction Program Hospital file.

The dataset includes hospital-level information such as:

- Facility name
- Facility ID
- State
- Medical-condition measure
- Excess Readmission Ratio
- Predicted Readmission Rate
- Expected Readmission Rate
- Measurement period

The application converts readmission-related fields to numeric values and removes records with missing values required for the rankings or visualizations.

Records suppressed by CMS because of small counts may be excluded when the required readmission measures are unavailable.

## Project Structure

```text
hospital-readmissions-dashboard-app/
├── app.py
├── README.md
├── requirements.txt
└── data/
    └── FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv
```
## Installation Instructions

Open a terminal in the project folder and install the required Python packages:

```bash
python3 -m pip install -r requirements.txt
```

## How to Run the Application

From the project folder, run:

```bash
python3 -m streamlit run app.py
```

If a browser does not open automatically, open:

```text
http://localhost:8501
```

The `README.md` file contains the project explanation and instructions. The `requirements.txt` file contains only the Python packages needed to run the application.

##Team Members

This dashboard was developed as a group project for BUS 601 at California State University, East Bay. 

- Harman Grewal
- Khanh Le
- Nishanth Palanisamy
- Alyssa Vasquez
