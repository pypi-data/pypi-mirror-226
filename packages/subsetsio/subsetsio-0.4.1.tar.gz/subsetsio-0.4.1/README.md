# Subsets Python SDK

Easily access the Subsets data warehouse using Python.

## Installation

Run the following command to install the SDK:

```pip install subsetsio```
## Usage


At the moment, you can only use the SDK for querying. To explore datasets, checking quotas, and viewing past queries, visit the subsets.io web interface.

```python
from subsets_python_sdk import query

# Query the data warehouse
df = query(sql="YOUR_SQL_QUERY_HERE", api_key="YOUR_API_KEY")
```