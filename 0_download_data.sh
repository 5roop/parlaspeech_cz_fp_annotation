curl --remote-name-all https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1785{/ParlaSpeech-CZ.v1.0.jsonl.gz,/ParlaSpeech-CZ.v1.0.part1.tgz,/ParlaSpeech-CZ.v1.0.part2.tgz,/ParlaSpeech-CZ.v1.0.part3.tgz,/ParlaSpeech-CZ.v1.0.part4.tgz}

gzip -dk ParlaSpeech-CZ.v1.0.jsonl.gz
for file in $(ls *.tgz)
do
    tar -xkvf $file
done

rm -f *gz