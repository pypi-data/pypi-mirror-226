# Subsets Python SDK

Easily access the Subsets data warehouse using Python.

## Installation

Copy the SDK code and include it in your project.

## Prerequisites

- Pandas: `pip install pandas`
- Requests: `pip install requests`

## Usage

```python
from subsets_python_sdk import query

# Query the data warehouse
df = query(sql="YOUR_SQL_QUERY_HERE", api_key="YOUR_API_KEY")