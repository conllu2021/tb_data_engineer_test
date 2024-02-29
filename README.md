# Tinybird Data Engineer Test

This repository contains my solution to the Data Engineer test, which you can find at https://gist.github.com/javisantana/a1962319a06dd1a05b14d5e9738c8f75.

My solution consists of a Python application that reads a parquet file from the NYC "Yellow Taxi" Trips Data website and generates a new local parquet file, including the rows greater than or equal to the 90th percentile for the trip_distance column.

## Installation

Please follow the next steps to run this application on your computer.

### Python installation

This application requires Python 3.8 or higher installed.

If you don't have Python installed, you can follow the next instructions to download and install the latest version of Python: https://wiki.python.org/moin/BeginnersGuide/Download.

### Repository downloading

After installing Python 3.8 or higher, the next step is to download this repository to a local folder. Please open a terminal and execute the following command:

```console
git clone https://github.com/conllu2021/tb_data_engineer_test.git
```

This instruction will create a new folder with the repository's name (tb_data_engineer_test). Run the following command to enter this new folder:

```console
cd tb_data_engineer_test
```

### Virtual environment creation

To finish the installation of this application, you should create a virtual environment:

```console
python3 -m venv venv
```

And then activate it:

```console
source venv/bin/activate
```

Once the virtual environment is activated, update the Python package installer (PIP) as shown next:

```console
python3 -m pip install --upgrade pip
```

And finally, install all dependencies of this application with the following command:

```console
pip install -r requirements.txt
```

## Usage

After completing the installation, you can start executing the application.

Please copy and paste the file URL and pass it to the application, as shown next. For example, for the URL https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-04.parquet, you would write:

```console
python3 main.py https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-04.parquet
```

Or you can download the file and append its path to the application:

```console
python3 main.py yellow_tripdata_2023-04.parquet
```

By default, the percentile applied is the 90th. If you want to replace it with another value, you can do it this way:

```console
python3 main.py yellow_tripdata_2023-04.parquet --percentile=95
```

If the execution goes fine, the application will create a new file with the prefix output_ (for instance, output_yellow_tripdata_2023-04.parquet) in the same folder, and it will show the following message:

```console
foo@bar:~$ python3 main.py yellow_tripdata_2023-04.parquet
Done!

```

You can read the help message of the application by running the following command:

```console
python3 main.py -h
```

## Technology decisions

This section reviews all the technologies I have used for this application.

### Python

Python is the lingua franca for using a programming language for data analysis. It is straightforward, robust, versatile, and has a vast community of users and multiple libraries. 

I have been using Python for the last eight years and am comfortable writing code with this language.

### DuckDB

I have decided to use DuckDB to load the parquet file and process it. DuckDB is an analytical SQL database that can quickly load and write parquet files.

The other options I have considered are pandas, Polars and PyArrow. Those libraries could have worked fine for this test, but I find DuckDB easier to use, and I wanted to use SQL as it is a requirement for the Data Engineer position.

I am very familiar with the SQL language.

### Linters 

Using linters for such a basic application might seem overkill, but the best way to write good code is to start with linters from scratch.

I have selected Pylint as static code analyser because it is the most complete code analyser for Python, even though it performs much worse than other alternatives like ruff.

On the other hand, I have added type annotations to the code. To make sure the static typing is correct, I have used mypy.

Finally, I have configured sqlfluff as a linter for the SQL code to make sure the query I have written is well-defined.

I have extensive experience in Pylint, mypy (I always type my Python code) and sqlfluff.

Anyhow, in an actual request from a Tinybird client, I would adapt my technologies and linters to the Tinybird standards.

## Further improvements

## Data quality

Concerning data quality, parquet files could contain rows with missing or wrong values. Ensuring incoming data are well-formed and meet our minimum quality requirements is very important.

In some cases, some outliers we detect in the table could be abnormal values, not outliers. For instance, in the data from NYC "Yellow Taxi" Trips, trips with distances greater than 500 miles, rows with a negative total amount or trips with more than 10 passengers (to give some examples) should be considered abnormal values, rather than extreme values.

I have not added any code to detect and remove low quality rows.

## Outlier detection

Although detecting outliers is a fundamental strategy for data analysis, there is no universally agreed-upon method for doing so.

However, fixing a constant percentile to detect extreme values from the NYC "Yellow Taxi" Trips Data might not be recommendable. Why? Every file could contain a different distribution of trip distances due to seasonal changes and modifications in the way data are collected, among other reasons.

Instead of applying the 90th percentile to every file, I suggest a simple method that adapts itself to the distribution of trip distances. This method is called the IQR rule, and it uses the interquartile range (IQR), which is calculated as the difference between the 25th and 75th percentile. Then, all the values lower than the 25th percentile minus IQR * 1.5 or greater than the 75th percentile plus IQR * 1.5 should be considered outliers. You could visualise the data using a boxplot that uses this strategy to show the outliers.

Given that the client is interested in detecting the outliers with the larger values (the distribution is right-skewed), we could return all the values greater than the 75th percentile plus IQR * 1.5.

Please take into account that with this method, we could find parquet files without outliers.

## Testing

I have not implemented any automatic test for this application. It would be interesting to add automatics tests to make sure the application works as we expect and avoid adding bugs in future modifications.

For that purpose, I would use pytest.

## Logging

In addition, I have not configured any logging system, for instance, to enable the program's execution in debugging mode. 

On the other hand, the error management of the application is very basic, and it could be improved when the application includes more functionality.

## Performance

I have not considered any performance requirements, even though the performance of DuckDB with parquet files of that size is excellent.

## Other ideas

- Add pre-commit to the project so the linters can be executed before every commit.
- Add Bandit as a linter for detecting common security issues in the code.
- And finally, reorganise the repository if this project grows in requirements.