# Twitter Sentiment Analysis

This project is about Sentiment Analysis of a desired Twitter topic with Apache Spark Structured Streaming, Apache Kafka, Python and AFINN Module. You can learn sentiment status of a topic that is desired.

For example; you might be curious about Game of Thrones’s new episode and you might get someone’s opinions about this new episode previously. Answer can be NEGATIVE, NEUTRAL or POSITIVE according to opinions.

## Code Explanation

1. Authentication operations were completed with Tweepy module of Python. You must take keys from Twitter API.
2. StreamListener named TweetListener was create for Twitter Streaming. StreamListener produces data for Kafka Topic named 'twitter'.
3. StreamListener also calculates Tweets' sentiment value with AFINN module and sends this value to 'twitter' topic.
4. Producing data was filtered about including desired topic.
5. Kafka Consumer that consumes data from 'twitter' topic was created.
6. Also, it converts streaming data to structured data. This structured data is placed into a SQL table named 'data'.
7. Data table has 2 columns named 'text' and 'senti_val'.
8. Average of sentiment values of senti_val column is calculated by pyspark.sql.functions.
9. Also, user defined function named fun is created for status column.
10. Status column has POSITIVE, NEUTRAL or NEGATIVE that change according to avg(senti_val) column in real-time.

## Running

1. Create Twitter API account and get keys for [twitter_config.py](https://github.com/kaantas/spark-twitter-sentiment-analysis/blob/master/twitter_config.py)
2. Start Apache Kafka
```
/bin/kafka-server-start.sh /config/server.properties
```
3. Run [tweet_listener.py](https://github.com/kaantas/spark-twitter-sentiment-analysis/blob/master/tweet_listener.py) with Python version 3 and desired topic name. <br>
```
PYSPARK_PYTHON=python3 bin/spark-submit tweet_listener.py "Game of Thrones"
```
4. Run [twitter_topic_avg_sentiment_val.py](https://github.com/kaantas/spark-twitter-sentiment-analysis/blob/master/twitter_topic_avg_sentiment_val.py) with Python version 3.
```
PYSPARK_PYTHON=python3 bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.1 twitter_topic_avg_sentiment_val.py
```
