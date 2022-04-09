from random import random
from operator import __add__

from pyspark.sql import SparkSession

spark = SparkSession\
    .builder\
        .appName('PythonPI')\
            .getOrCreate()