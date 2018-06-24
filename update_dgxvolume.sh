#!/bin/bash

cp _drafts/dgxvolume.template dgxvolume.markdown
cd dgxvolume_scripts
./current_block.sh
python3 digix_info_bot.py >> ../dgxvolume.markdown
gnuplot graph.gp
./eps2png.sh out.eps
cd ..

