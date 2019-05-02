TAGGER=./bin/tnt -v0 -H models/hindi  # Use option -u1 for speed at a slight cost of precision. For more options use ./bin/tnt -h
LEMMATIZER=python2 ./bin/lemmatiser.py models/hindi.lemma
TAG2VERT=python2 ./bin/tag2vert.py
NORMALIZE=python2 ./bin/normalize_vert.py
POSMOD=python2 ./bin/modify_pos.py
TOKENIZER=python2 ./bin/unitok.py -l hindi -n

tag: 
	cat hindi.input.txt | $(TOKENIZER) | sed -e 's/।/./g' | sed -e 's/^\.$$/.\n<\/s>\n<s>/g' |  $(NORMALIZE)  > hindi.tmp.words
	$(TAGGER) hindi.tmp.words | sed -e 's/\t\+/\t/g' | $(LEMMATIZER) | $(TAG2VERT) > hindi.output
	rm hindi.tmp.words
	echo "Output stored in hindi.output"
