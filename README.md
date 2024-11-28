# Stock Market Indices Data Pipeline with Apache Airflow

## Overview
This project demonstrates the use of **Apache Airflow** to create an end-to-end data pipeline that:
1. Scrapes the web to retrieve the component companies of the **Nasdaq-100**, **S&P-500**, and **DJI-30** indices.
2. Fetches the latest stock prices for each company using the **yfinance** API.
3. Saves the data into a **CSV file** and a **MySQL database** for storage and further analysis.

This project showcases how modern tools can be integrated to automate data collection, transformation, and storage tasks, providing a foundation for scalable and efficient data engineering workflows.

---

## Features
- **Web Scraping**: Dynamically collects the latest component companies of major stock indices.
- **Stock Price Retrieval**: Uses `yfinance` to fetch up-to-date stock prices for listed companies.
- **Data Storage**:
  - CSV file for quick access and sharing.
  - MySQL database for long-term storage and seamless integration with analytics pipelines.
- **Apache Airflow**: Automates the entire process using Directed Acyclic Graphs (DAGs).

---

## Requirements
### Tools and Libraries
- **Apache Airflow** (tested on GitHub Codespaces)
- **Python 3.9+**
- **MySQL**
- Python Libraries:
  - `yfinance`
  - `requests`
  - `pandas`
  - `mysql-connector-python`

### Infrastructure
- GitHub Codespaces (recommended for running Airflow if local virtualization is unavailable).
- A MySQL database instance (local or cloud-based).

---

## Setup
### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MySQL Database
- Create a MySQL database to store stock data.
- Update the Airflow connection settings for MySQL in the **Airflow UI** or set up an environment variable for connection details.

### 4. Set Up Apache Airflow
- Initialize Airflow:
  ```bash
  airflow db init
  ```
- Start the Airflow webserver and scheduler:
  ```bash
  airflow webserver &
  airflow scheduler &
  ```
- Access the Airflow UI at `http://localhost:8080`.
- Upload the DAG file to the `dags/` folder.

### 5. Run the Pipeline
- Trigger the DAG manually via the Airflow UI or set a schedule for automation.

---

## Workflow
1. **Web Scraping Task**: Scrapes websites to extract the list of companies in Nasdaq-100, S&P 500, and DJI-30 indices.
2. **Stock Price Fetching Task**: Calls the `yfinance` API to fetch stock prices for the extracted companies.
3. **Data Transformation Task**: Cleans and organizes the retrieved data.
4. **Data Storage Task**:
   - Saves the transformed data into a CSV file.
   - Inserts the data into the MySQL database.

---

## Challenges and Learnings
1. **Setting Up Apache Airflow**:
   - Faced virtualization issues on the local machine, leading to the discovery and use of **GitHub Codespaces** for the setup.
2. **Workflow Debugging**:
   - Addressed API rate limits and handled dynamic changes in web-scraped content.
3. **Data Pipeline Optimization**:
   - Designed the pipeline for modularity and scalability to accommodate future enhancements.

---

## Future Enhancements
- Implement data validation and error logging to improve reliability.
- Schedule the DAG to run daily for automatic updates.
- Build visualizations to analyze stock price trends using the stored MySQL data.
- Integrate with a cloud database for greater scalability.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments
Special thanks to the open-source community for providing tools like Apache Airflow and yfinance, which make projects like this possible.



