# Superstore-Sales-Analysis-and-Customer-Segmentation
This project focuses on analyzing sales data from a retail company to understand customer purchase behavior and sales performance. The aim is to provide actionable insights that can help in making data-driven decisions for marketing strategies, inventory management, and customer retention.

Objectives

    Identify the top-selling products.
    Determine which states generate the highest sales.
    Analyze yearly sales trends.
    Segment customers based on their purchasing behavior.
    Assess the impact of discounts on sales and profit.
    Understand regional sales performance.

Features

    Data Preprocessing: Handling missing values, converting data types, and calculating total sales amount.
    Sales and Product Analysis: Insights into total sales by state, top-selling products, and yearly sales trends.
    Customer Segmentation: RFM (Recency, Frequency, Monetary) analysis to segment customers based on their purchase behavior.
    Discount Impact Analysis: Assessing the effect of discounts on sales and profit.
    Interactive Dashboard: A Dash-based interactive dashboard for visualizing key metrics and trends.

Requirements:
    Python 3.11
    MySQL
    Python libraries: pandas, mysql-connector-python, plotly, dash, mlxtend
    Gitbash

#HOW TO RUN


1. MySQL Database Setup
    	Copy and Paste the sql script into Mysql

2. Install the required libraries 
	pip install pandas mysql-connector-python plotly dash mlxtend

3. Open Gitbash and run python database.py

	-This script will perform the following analyses:

   	 	  -Total Sales by State
   		  -Top 5 Products by Total Sales
    		  -Top 4 Years by Total Sales
    		  -RFM Analysis

4. Run python market2.py
	This script will perform additional analyses and present a dashboard:

   		 -Profit by Product Category
   		 -Monthly Sales Trend
                 -Customer Segmentation Analysis
   		 -Region-wise Sales Performance
   		 -Discount Impact on Sales and Profit

5. To view dashboard
	Open a web browser and navigate to http://127.0.0.1:8050/

