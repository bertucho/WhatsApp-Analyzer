WhatsApp-Analyzer

Calculates what are the most frecuent words in a WhatsApp exported conversation file.

Example to get how many words have been written by day (ordered by date) and exported to a file:

conver_handler = WsappConver(filepath)
all_words = conver_handler.get_ordered_density_words()
ordered_words = OrderedDict()
for key, value in sorted(all_words.items(), key=lambda t: t[1], reverse=True):
	ordered_words[key] = value
with io.open("words_frecuency.txt", "w", encoding="utf8") as f:
	f.write("Word\tOcurrencias\n")
	for key,value in ordered_words.items():
		f.write(str(key)+"\t"+str(value)+"\n")

