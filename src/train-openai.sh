#!/bin/bash

model="davinci" # Best results
dataset="rsc/custom.jsonl"

print_usage() {
    echo "sh train-openai.sh # Train default model (davinci) with rsc/custom.jsonl"
    echo "sh train-openai.sh -m <MODEL_NAME> -f <FILE> # Train custom model with custom dataset"
    echo "sh train-openai.sh -h # Show this message"
}

while getopts ":h:d:m:" o; do
    case "${o}" in
        s)
            dataset=${OPTARG}
            ((s == 45 || s == 90)) || usage
            ;;
        p)
            model=${OPTARG}
            ;;
        *)
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${model}" ] || [ -z "${dataset}" ]; then
    usage
fi

openai api fine_tunes.create -m ${model} --n_epochs 2 -t ${dataset}
