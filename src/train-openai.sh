#!/bin/bash

model="davinci" # Best results
dataset="rsc/custom.jsonl"

print_usage() {
    echo "sh train-openai.sh # Train default model (davinci) with rsc/custom.jsonl"
    echo "sh train-openai.sh -m <MODEL_NAME> -f <FILE> # Train custom model with custom dataset"
    echo "sh train-openai.sh -h # Show this message"
}

while true; do
  case "$1" in
    -h | --help ) print_usage; shift; exit 0 ;;
    -d | --dataset ) dataset=$2; shift ;;
    -m | --model ) model="$2"; shift ;;
    * ) print_usage; shift; exit 1 ;;
  esac
done

openai api fine_tunes.create -m ${model} --n_epochs 2 -t ${dataset}
