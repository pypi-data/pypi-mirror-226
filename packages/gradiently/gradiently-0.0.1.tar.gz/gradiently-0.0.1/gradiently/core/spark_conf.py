from dataclasses import dataclass


@dataclass
class SparkConf:
    app_name: str
    master: str
    executor_memory: str
    driver_memory: str
    num_executors: int
    spark_properties: dict = None
    credentials: dict = None

    def get_spark_config(self):
        config = {
            "spark.app.name": self.app_name,
            "spark.master": self.master,
            "spark.executor.memory": self.executor_memory,
            "spark.driver.memory": self.driver_memory,
            "spark.executor.instances": str(self.num_executors),
        }

        if self.spark_properties:
            config.update(self.spark_properties)

        if self.credentials:
            config.update(self.credentials)

        return config
