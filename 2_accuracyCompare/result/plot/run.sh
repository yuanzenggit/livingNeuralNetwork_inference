
for i in 0 1 2 3 4
do 
    grep 'test epochs*' comp_$i > ./Computational_Val_$i
done


for i in 5 6 7 8 9
do 
    grep 'test epochs*' comp_$i > ./Computational1_Val_$i
done

for i in 5 6 7 8 9
do 
		grep 'test  iter*' biophy_$i > ./Biophysical_Val_$i
done

for i in 0 1 2 3 4
do 
		grep 'test  iter*' biophy_$i > ./Biophysical1_Val_$i
done

