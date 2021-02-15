for i in 6 7 8 9 10
do 
		grep 'test:*' biophy_$i > ./result/Biophysical_Val_$i
done


for i in 0 1 2 3 4 5 6 7 8 9  
do 
		grep 'test:*' trial_$i > ./result/Computational_Val_$i
done
