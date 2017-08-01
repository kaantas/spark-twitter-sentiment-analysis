import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import twitter_config
import pykafka
from afinn import Afinn
import sys

class TweetListener(StreamListener):
	def __init__(self):
		self.client = pykafka.KafkaClient("localhost:9092")
		self.producer = self.client.topics[bytes('twitter','ascii')].get_producer()

	def on_data(self, data):
		try:
			json_data = json.loads(data)

			send_data = '{}'
			json_send_data = json.loads(send_data)			
			json_send_data['text'] = json_data['text']
			json_send_data['senti_val']=afinn.score(json_data['text'])

			print(json_send_data['text'], " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ", json_send_data['senti_val'])

			self.producer.produce(bytes(json.dumps(json_send_data),'ascii'))
			return True
		except KeyError:
			return True

	def on_error(self, status):
		print(status)
		return True

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: PYSPARK_PYTHON=python3 /bin/spark-submit ex.py <YOUR WORD>", file=sys.stderr)
		exit(-1)
	
	word = sys.argv[1]

	consumer_key = twitter_config.consumer_key
	consumer_secret = twitter_config.consumer_secret
	access_token = twitter_config.access_token
	access_secret = twitter_config.access_secret

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	
	# create AFINN object for sentiment analysis
	afinn = Afinn()

	twitter_stream = Stream(auth, TweetListener())
	twitter_stream.filter(languages=['en'], track=[word])
