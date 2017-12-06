cat large.txt | python model-mapper.py > junk
sort junk > test
rm junk
echo "map1 finished"
cat test | python model-reducer.py > features
echo "red1 finished"
cat test.txt | python part3-mapper.py > test3
echo "map2 finished"
cat test3 | python part4-reducer.py > test4
echo "red2 finished"
sort -f test4 > sortT
python compare.py sortT sortT2