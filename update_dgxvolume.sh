#!/bin/bash

cp _drafts/dgxvolume.template dgxvolume.markdown
cd /home/thomas/bandityui.github.io/dgxvolume_scripts 
./current_block.sh
python3 digix_info_bot.py >> ../dgxvolume.markdown
gnuplot graph.gp
./eps2png.sh out.eps
cd /home/thomas/bandityui.github.io/
git add .
git commit -m "."
git push -u origin master

