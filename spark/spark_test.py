from pyspark import SparkContext

# Spark instance
sc = SparkContext()

nums = sc.parallelize([1,2,3,4])

print(nums.take(1))