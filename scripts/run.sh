# This scripts runs an Advent of Code solution for the day and part specified

if [ ${#1} -gt 1 ]
then
    day_num=$1
else
    day_num=0$1
fi

cd ./solutions/day-$day_num

python part-$2.py