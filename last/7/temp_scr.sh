head -500 clean_pos.txt | tail -50 > test_pos.txt
head -500 clean_neg.txt | tail -50 > test_neg.txt
head -450 clean_pos.txt> train_pos.txt
tail -0 clean_pos.txt>> train_pos.txt
head -450 clean_neg.txt> train_neg.txt
tail -0 clean_neg.txt>> train_neg.txt
./createvoc.sh train_neg.txt train_pos.txt
echo 'Training and testing data created'
