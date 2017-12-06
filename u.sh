cat test.txt | python unixVersion.py large.txt > unixTest
sort -f unixTest > unixSorted
python compare.py unixSorted sortT2
