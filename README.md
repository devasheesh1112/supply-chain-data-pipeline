# Supply Chain Data Engineering Pipeline

## Overview

## Architecture

## Tech Stack

## Dataset

## Data Pipeline

## Data Quality

## PostgreSQL Data Model

## SQL Analytics

## Streamlit Dashboard

## Project Structure

## How to Run

## Key Engineering Decisions

## Results

## Future Improvements




             CSV DATA
                │
                ▼
        Python Ingestion
                │
                ▼
          PySpark ETL
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
     Orders  Inventory Suppliers
        │       │        │
        └───────┼────────┘
                ▼
         Data Quality
                │
                ▼
          Gold Dataset
                │
                ▼
          PostgreSQL
                │
        ┌───────┴───────┐
        ▼               ▼
   SQL Analytics   Streamlit



## Dashboard d

![Supply Chain Dashboard](docs/dashboard.png)