"""Custom exceptions for airflow_trigger_multiple_dag_run plugin."""
from airflow.exceptions import AirflowException


class NoDagRunsToMonitor(AirflowException):
    """No DagRuns to monitor by the sensor"""
