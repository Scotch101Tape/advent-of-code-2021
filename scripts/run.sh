# This scripts runs an Advent of Code solution for the day and part specified

if [ ${#1} -gt 1 ]
then
    day_num=$1
else
    day_num=0$1
fi

cd ./solutions/day-$day_num

if ( test -f "part-$2.py"; )
then
    python part-$2.py
elif ( test -f "part-$2.jl"; )
then
    julia part-$2.jl
else
    cd ./part-$2
    cargo run
fi