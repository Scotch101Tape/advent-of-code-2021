if [ ${#1} -gt 1 ]
then
    day_num=$1
else
    day_num=0$1
fi

cd ./solutions
mkdir day-$day_num

cd ./day-$day_num
touch input.txt

echo 'input = open("input.txt", "r")' > part-1.py
echo 'input = open("input.txt", "r")' > part-2.py