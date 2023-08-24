Wrapper to create Spark Connect session for Applications in Ocean

spark = OceanSparkSession.builder.appId("app-id").getOrCreate()