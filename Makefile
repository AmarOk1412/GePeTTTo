dataset:
	source env
	./src/gpt3-make-dataset.py

train:
	source env
	./src/train-openai.sh

answer:
	source env
	./src/answer-last.py