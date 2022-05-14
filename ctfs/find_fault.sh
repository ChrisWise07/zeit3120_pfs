i=-50
r=0
while [ $r -eq 0 ]
do
    i=$((i+1))
    python3 -c "print('a'*$i)" | ./a.out | grep "exit"
done
echo $i