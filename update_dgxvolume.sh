#!/bin/bash

cp /home/thomas/bandityui.github.io/dgxvolume_scripts/24hr_volume.dat /home/thomas/bandityui.github.io/dgxvolume_scripts/24hr_volume.backup
cp /home/thomas/bandityui.github.io/_drafts/dgxvolume.template /home/thomas/bandityui.github.io/dgxvolume.markdown
cd /home/thomas/bandityui.github.io/dgxvolume_scripts 
./current_block.sh
python3 digix_info_bot.py >> ../dgxvolume.markdown
gnuplot graph.gp
./eps2png.sh out.eps
cd /home/thomas/bandityui.github.io/
git add .
git commit -m "."
git push -u origin master

