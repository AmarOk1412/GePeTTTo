include env
export

dataset:
	./src/gpt3-make-dataset.py

train:
	./src/train-openai.sh

answer:
	./src/answer-last.py