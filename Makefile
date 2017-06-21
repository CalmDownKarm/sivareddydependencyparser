TAGGER=./hindi-pos-tagger/bin/tnt -v0 -H hindi-pos-tagger/models/hindi
LEMMATIZER=python2 ./hindi-pos-tagger/bin/lemmatiser.py hindi-pos-tagger/models/hindi.lemma
TAG2VERT=python2 ./bin/tag2vert.py
NORMALIZE=python2 ./bin/normalize_vert.py
POSMOD=python2 ./bin/modify_pos.py
ADDDUMMY=python2 ./bin/add_dummy_word.py
MERGE=python2 ./bin/merge.py
CONVERT_NULL=python2 ./bin/convert_NULL.py
CONVERT_FORMAT=python2 ./bin/convert_format.py
TOKENIZER=python2 ./bin/unitok.py -l hindi -n 

# Normalizer replaces some of the spellings with easy spellings on which the parser or MT systems work very well. 

%.output: %.input.txt
	# uncomment below line if you require a normalizer
	cat $< | $(TOKENIZER) | sed -e 's/।/./g' | sed -e 's/^\.$$/.\n<\/s>\n<s>/g' |  $(NORMALIZE)  > $@.tmp.words
	# uncomment below line if you do not require a normalizer
	# cat $< | $(TOKENIZER) |  sed -e 's/।/./g' | sed -e 's/^\.$$/.\n<\/s>\n<s>/g'  > $@.tmp.words
	$(TAGGER) $@.tmp.words | sed -e 's/\t\+/\t/g' | $(LEMMATIZER) | $(TAG2VERT) | $(POSMOD) | cut -f1,2,3 > $@.tmp.tag
	python2 bin/convert_format.py $@.tmp.tag $@.tmp.tag.conll
	java -jar bin/malt.jar -c test_complete -i $@.tmp.tag.conll -o $@.tmp.output -m parse
	python2 bin/convert_output.py $@.tmp.output $@
	rm  *.tmp.*
	echo "Output stored in $@"

clean:
	rm  *.tmp.*

