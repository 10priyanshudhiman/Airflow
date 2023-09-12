# imports for DAG

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

# defining DAG arguments

default_args = {
    'owner': 'Priyanshu Dhiman',
    'start_date': days_ago(0),
    'email': ['priyanshud310@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG
dag = DAG(
    dag_id='ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule=timedelta(days=1),
)

# defining the tasks
# defining the first task unzip_data

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xzf /home/project/airflow/dags/finalassignment/tolldata.tgz/tolldata.tgz',
    dag=dag
)

# defining the second task extract_data_from_csv

extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d"," -f1,2,3,4 vehicle-data.csv --output-delimiter="," > csv_data.csv',
    dag=dag
)

# defining the third task extract_data_from_tsv

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -f5,6,7 tollplaza-data.tsv --output-delimiter="," > tsv_data.csv',
    dag=dag
)

# defining the fourth task extract_data_from_fixed_width

extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command=' awk "NF{print $(NF-1) "," $NF}" payment-data.txt > fixed_width_data.csv',
    dag=dag
)

# Consolidating the data

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste -d "," csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv',
    dag=dag
)

transform_data = BashOperator(
    task_id='transform_data',
    bash_command='awk "BEGIN {FS = OFS = ","} {$4 = toupper($4)} 1" extracted_data.csv > transformed_data.csv',
    dag=dag

)

#pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data


