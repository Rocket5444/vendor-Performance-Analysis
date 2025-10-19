# Vendor Performance & Inventory Analysis

This project analyzes vendor sales, purchasing, and inventory data to identify key performance metrics, uncover trends, and pinpoint high-performing and at-risk brands. The workflow begins with ingesting raw data into an SQLite database, followed by data cleaning, feature engineering, and exploratory analysis in Python. The final, summarized dataset is used for in-depth analysis and to build metrics in a BI tool (like Power BI).

## Project Workflow

1.  **Data Ingestion**: Raw CSV files (e.g., purchases, sales, vendor invoices) located in a `data/` directory are loaded into an `inventory.db` SQLite database. (Handled by `Untitled.ipynb` / `ingestion_db.py`).
2.  **Data Transformation**: A Python script (`get_vendor_summary.py`) queries the database, joins the relevant tables, and performs data cleaning. It then engineers new features like `GrossProfit`, `ProfitMargin`, `StockTurnover`, and `SalesToPurchaseRatio`.
3.  **Data Export**: The final, cleaned, and aggregated data is saved as `vendor_sales_summary.csv`.
4.  **Analysis**:
    * `Exploratory Data Analysis.ipynb`: Initial exploration of the summarized data to understand distributions, correlations, and data quality.
    * `Vendor Performance Analysis.ipynb`: Deeper statistical analysis to compare vendor performance, identify top/low performers, and test hypotheses (e.g., comparing profit margins of different vendor groups).
5.  **BI Dashboarding**: The `vendor_sales_summary.csv` is loaded into a BI tool, where DAX measures are created to build interactive dashboards for monitoring key metrics.

## File Descriptions

* `get_vendor_summary.py`: Main Python script to run the ETL process. It connects to `inventory.db`, runs a SQL query to join tables, cleans the resulting DataFrame, adds new calculated columns, and saves the output.
* `Vendor Performance Analysis.ipynb`: Jupyter Notebook containing detailed analysis, hypothesis testing (e.g., T-tests), and visualization of vendor performance.
* `Exploratory Data Analysis.ipynb`: Jupyter Notebook for initial data checks, cleaning steps (like handling infinities in `ProfitMargin`), and basic visualizations.
* `Untitled.ipynb`: (Assumed to be `ingestion_db.ipynb`) A notebook containing the Python script to load raw CSVs from a `/data` folder into the `inventory.db` SQLite database.
* `vendor_sales_summary.csv`: The final, processed dataset used for analysis and dashboarding. This is the single source of truth for the analysis notebooks and BI dashboard.

## Key Metrics & DAX Formulas

The following metrics are central to this analysis, implemented as DAX measures in the Power BI report.

### Brand & Vendor Performance

* **Brand Performance Summary**: Creates a summary table of brands, their total sales, and average profit margin.
    ```dax
    BrandPerformance = SUMMARIZE(
        vendor_sales_summary, 
        vendor_sales_summary[Description], 
        "TotalSales", SUM(vendor_sales_summary[TotalSalesDollars]), 
        "AvgProfitMargin", AVERAGE(vendor_sales_summary[ProfitMargin])
    )
    ```
* **Target Brands**: Identifies high-potential "target" brands that are in the bottom 15% for sales but in the top 85% for profit margin.
    ```dax
    TargetBrand = 
    IF(
        [TotalSales] <= PERCENTILEX.EXC(BrandPerformance, BrandPerformance[TotalSales], 0.15) 
        && [AvgProfitMargin] >= PERCENTILEX.EXC(BrandPerformance, BrandPerformance[AvgProfitMargin], 0.85), 
        "Yes", 
        "No"
    )
    ```

### Purchase & Contribution

* **Purchase Contribution by Vendor**: Calculates the total purchase dollars for each vendor.
    ```dax
    PurchaseContribution = SUMMARIZE(
        vendor_sales_summary, 
        vendor_sales_summary[VendorName], 
        "TotalPurchaseDollars", SUM(vendor_sales_summary[TotalPurchaseDollars])
    )
    ```
* **Purchase Contribution %**: Calculates each vendor's share of the total purchases.
    ```dax
    PurchaseContribution% = 
    PurchaseContribution[TotalPurchaseDollars] / sum(PurchaseContribution[TotalPurchaseDollars]) * 100
    ```

### Inventory & Capital

* **Unsold Capital**: Estimates the capital tied up in unsold inventory for each product.
    ```dax
    UnsoldCapital = 
    (vendor_sales_summary[TotalPurchaseQuantity] - vendor_sales_summary[TotalSalesQuantity]) 
    * vendor_sales_summary[PurchasePrice]
    ```
* **Low Turnover Vendors**: Creates a table summarizing vendors with a stock turnover ratio of less than 1 (i.e., not selling all purchased stock).
    ```dax
    LowTurnoverVendor = 
    VAR FilteredData = FILTER(
        vendor_sales_summary, 
        vendor_sales_summary[StockTurnover] < 1
    )
    RETURN
        SUMMARIZE(
            FilteredData, 
            vendor_sales_summary[VendorName], 
            "AvgStockTurnOver", AVERAGE(vendor_sales_summary[StockTurnover])
        )
    ```

## How to Run

1.  **Environment Setup**: Ensure you have Python and the required libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `sqlite3`) installed.
    ```bash
    pip install pandas numpy matplotlib seaborn scipy
    ```
2.  **Place Data**: Create a `data/` folder in the root directory and place all raw CSV files inside it.
3.  **Ingest Data**: Run the `Untitled.ipynb` (or equivalent ingestion script) to create the `inventory.db` file.
4.  **Process Data**: Execute the `get_vendor_summary.py` script to generate the `vendor_sales_summary.csv` file.
    ```bash
    python get_vendor_summary.py
    ```
5.  **Run Analysis**: Open and run the Jupyter Notebooks (`Exploratory Data Analysis.ipynb`, `Vendor Performance Analysis.ipynb`) to see the data analysis and visualizations.
6.  **View Dashboard**: Open the associated Power BI file (or other BI tool) and connect it to the `vendor_sales_summary.csv` to interact with the dashboard.

---

### Project By - Kunal
