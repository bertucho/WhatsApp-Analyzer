import nltk, re, io
from datetime import datetime
from stopwords import stopwords

class WsappConver:

	def __init__(self, filename):
		'''
		It process the WhatsApp conversation file and creates a data structure with date, time,
		author and text of each message
		'''
		self.words_by_date = {}
		self._filename = filename
		self.conver = []
		msg_dict = {}
		date = None
		time = None
		author = None
		text = None
		with io.open(filename, "r", encoding="utf8") as f:
			for line in f:
				message = re.search("^(\d\d?/\d\d?/\d\d),\s(\d\d?:\d\d)\s-\s([a-zA-Z0-9_\s]*):\s(.*)", line)
				if message:
					date = message.group(1)
					time = message.group(2)
					author = message.group(3)
					text = self.remove_emojis(message.group(4))
					self.conver.append({
							'date': date,
							'time': time,
							'author': author,
							'text': text
						})
				else: #puede ser un mensaje con salto de linea
					if author and date and time:
						self.conver[-1]['text'] += " "+self.remove_emojis(line)


	def remove_emojis(self, text):
		return re.sub(r'[^\x00-\x7Fá-úÁ-ÚñÑüÜ¿¡çÇ]+',' ', text)
				

	def get_word_frecuency(self, word):
		''' Calculates how many times a word is repeated in all the conversation'''
		for msg in self.conver:
			if word in msg["text"].lower():
				#print(msg["text"], flush=True)
				date = msg["date"]
				author = msg["author"]
				if date in self.words_by_date:
					if author in self.words_by_date[date]:
						self.words_by_date[date][author] += 1
					else:
						self.words_by_date[date][author] = 1
				else:
					self.words_by_date[date] = {}
					self.words_by_date[date][author] = 1
		#for key, value in self.words_by_date.items():
		#	self.words_by_date[key] = value/self.get_words_by_date(key)*100
		return self.words_by_date


	def get_regex_frecuency(self, regex):
		''' Calculates how many times a match with regex is repeated in all the conversation'''
		for msg in self.conver:
			if re.match(regex, msg["text"].lower()):
				print(msg["text"], flush=True)
				date = msg["date"]
				author = msg["author"]
				if date in self.words_by_date:
					if author in self.words_by_date[date]:
						self.words_by_date[date][author] += 1
					else:
						self.words_by_date[date][author] = 1
				else:
					self.words_by_date[date] = {}
					self.words_by_date[date][author] = 1
		return self.words_by_date


	def get_words_ocurrences(self, words):
		pass


	def get_words(self):
		return self.words_by_date


	def get_words_frecuency(self):
		''' Calculates the relative frecuency of each of the words'''
		words_frec = {}
		for key, value in self.words_by_date.items():
			words_frec[key] = value/self.get_words_by_date(key)*1000
		return words_frec


	def get_words_by_date(self, date):
		cnt = 0
		arg_date = datetime.strptime(date, "%d/%m/%y").date()
		for msg in self.conver:
			msg_date = datetime.strptime(msg["date"], "%d/%m/%y").date()
			if msg_date > arg_date:
				break
			cnt += len(msg["text"].split())
		return cnt


	def get_ordered_density_words(self):
		''' Calculates the top more frecuent words of the conversation '''
		self.density = {}
		for msg in self.conver:
			#words = msg["text"].lower().split()
			words = re.findall(r"[\w':;()]+", msg["text"].lower())
			for word in words:
				word = str(word)
				if word in stopwords:
					continue
				if word in self.density:
					self.density[word] += 1
				else:
					self.density[word] = 1
		return self.density