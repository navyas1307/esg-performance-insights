# ESG Performance Insights

Welcome to **ESG Performance Insights**, an interactive platform designed to provide comprehensive insights into companies' **Environmental, Social, and Governance (ESG)** performance. This tool helps organizations, investors, and stakeholders evaluate corporate sustainability efforts with the help of intuitive visualizations, detailed analysis, and actionable recommendations.

---

## Table of Contents

1. [Overview](#overview)
2. [Purpose of the Project](#purpose-of-the-project)
3. [How Data is Sourced](#how-data-is-sourced)
4. [Features](#features)
5. [Technologies Used](#technologies-used)
6. [File Structure](#file-structure)
7. [Conclusion](#Conclusion)

---

## Overview

**ESG Performance Insights** allows users to explore and analyze the **ESG performance** of companies across various sectors. Using data visualizations and benchmarking tools, users can identify companies' strengths and weaknesses in environmental impact, social responsibility, and governance practices.

---

## Purpose of the Project

The primary goal of **ESG Performance Insights** is to provide businesses and stakeholders with an easy-to-use platform that helps them:

- **Assess ESG performance**: Gain insights into how companies are performing in terms of sustainability and ethical practices.
- **Benchmark performance**: Compare a company’s ESG performance with its industry peers.
- **Identify areas for improvement**: Receive actionable suggestions to enhance ESG scores.
- **Spot controversial sectors**: Understand which sectors may involve controversial business practices and which companies are most impacted.

In a world where sustainability is becoming increasingly important, this project enables stakeholders to make informed decisions that align with their values.

---

## How Data is Sourced

The data used in this project is primarily sourced from **Yahoo Finance**. This includes publicly available company financial data and performance metrics, such as:

- **Total ESG Score**: The overall ESG score for each company, representing environmental, social, and governance practices.
- **Environment, Social, and Governance Scores**: Breakdown of each ESG category.
- **Controversy**: The highest controversy level associated with each company.

**Yahoo Finance** API was utilized to pull the necessary data regarding stock tickers, ESG scores, and financial performance metrics for global companies. The data helps provide accurate and up-to-date performance metrics, essential for making informed evaluations and recommendations.

---

## Features

The platform offers the following key features:

### 1. **Peer Company Comparison**
   - **Peer Comparison** allows you to see how a company's ESG performance compares with its competitors in the same sector. This feature helps to evaluate how well a company is performing in terms of sustainability and governance relative to its peers. 
   - Users can identify if the selected company is leading or lagging in its sector's ESG practices.
   - **Example:** If the selected company scores an ESG of 75 while its peers in the same industry have scores ranging from 50 to 70, this suggests that the selected company is performing better in terms of ESG sustainability.

### 2. **Suggestions for Improvement**
   - Based on the analysis of ESG scores and performance, **Suggestions for Improvement** offer actionable recommendations for the selected company. These recommendations target specific areas of improvement in the **Environmental**, **Social**, and **Governance** dimensions.
   - **Example:** If a company has a low social score, the platform may suggest steps to improve employee welfare, community engagement, or labor practices to enhance its social responsibility.
   - Recommendations could include:
     - **Environment**: Implement sustainable energy practices, reduce carbon footprint.
     - **Social**: Improve employee health and safety standards, enhance diversity and inclusion.
     - **Governance**: Strengthen board oversight, increase transparency in decision-making.
---

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
  - **Plotly.js**: A powerful JavaScript library used for creating interactive visualizations such as bar charts, scatter plots, and radar charts.
  - **Jinja2**: Templating engine used for dynamically rendering content on the HTML pages.
  
- **Backend**: Flask (Python)
  - Used for dynamically generating pages and managing the flow of data to the front end.

- **Other Libraries**: 
  - **Plotly (Python)**: For creating visualizations that are then passed to the frontend.
  - **Bootstrap**: Used for responsive design and layout management (if applicable).

---


## File Structure
/esg-performance-insights/
│
├── /static/             # Static resources like CSS
│   └── /css/            
│       └── styles.css   
│
├── /templates/                  # HTML templates go here
│   ├── index.html               # Main page
│   ├── results.html             # Analysis results page
│   ├── terms_and_services.html  # Terms and Services page
│   ├── privacy_policy.html      # Privacy Policy page
│   └── (other HTML files if necessary)
│
├── /data/               
│   └── esg_data.csv     
│
├── format.py            # File to handle data formatting operations
├── extraction.py        # File to handle data extraction (e.g., Yahoo Finance)
├── app.py               # Python app for backend logic
├── README.md            # Project documentation
└── requirements.txt     # List of dependencies (e.g., pandas, plotly)




## Conclusion

**ESG Performance Insights** provides valuable insights into the environmental, social, and governance (ESG) practices of companies, offering users a comprehensive way to assess corporate sustainability. By leveraging data sourced from Yahoo Finance, the platform enables easy comparison between companies' ESG performance and suggests actionable steps to improve sustainability and governance practices.

This tool empowers businesses, investors, and other stakeholders to make informed decisions based on up-to-date ESG data. Whether you're looking to evaluate a company's ESG score or understand where a company stands in comparison to its industry peers, **ESG Performance Insights** provides the necessary tools and visualizations to enhance your decision-making process.

With continuous improvements and data updates, this platform will serve as a valuable resource for anyone interested in sustainable business practices and ethical investment.

