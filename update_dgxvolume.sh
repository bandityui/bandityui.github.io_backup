#!/bin/bash

cp /home/thomas/bandityui.github.io/_drafts/dgxvolume.template /home/thomas/bandityui.github.io/dgxvolume.markdown
cd /home/thomas/bandityui.github.io/dgxvolume_scripts 
python3 weekly_volume.py >> ../dgxvolume.markdown
gnuplot graph_weekly.gp
./eps2png.sh out.eps
cd /home/thomas/bandityui.github.io/
git add .
git commit -m "."
git push -u origin master

