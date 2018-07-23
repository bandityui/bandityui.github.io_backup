#!/bin/bash

cp /home/thomas/bandityui.github.io/_drafts/dgxvolume.template /home/thomas/bandityui.github.io/dgxvolume.markdown
cd /home/thomas/bandityui.github.io/dgxvolume_scripts 
python3 wv.py >> ../dgxvolume.markdown
gnuplot graph_weekly.gp
gnuplot graph_daily.gp
gnuplot graph_fees.gp
./eps2png.sh out.eps
./eps2png.sh daily.eps
./eps2png.sh fees.eps
A=$(cat date.txt)
cd /home/thomas/bandityui.github.io/
sed -i "s/VALUE/$A/" dgxvolume.markdown
git add .
git commit -m "."
git push -u origin master

