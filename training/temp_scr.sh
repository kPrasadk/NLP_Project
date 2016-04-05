cat clean_pos.txt | head -50 | tail -50 > test_pos.txt
cat clean_neg.txt | head -50 | tail -50 > test_neg.txt
cat clean_pos.txt | head -0> train_pos.txt
cat clean_pos.txt | tail -450>> train_pos.txt
cat clean_neg.txt | head -0> train_neg.txt
cat clean_neg.txt | tail -450>> train_neg.txt
./createvoc.sh train_neg.txt train_pos.txt
echo 'Training and testing data created'
