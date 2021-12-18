# This script publishes to github the solution for the day specified

if [ ${#1} -gt 1 ]
then
    day_num=$1
else
    day_num=0$1
fi

git add ./solutions/day-$day_num
git commit -m "Finish Day $1"
git push
