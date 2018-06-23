#!/bin/bash

cp _drafts/dgxvolume.template dgxvolume.markdown
cd dgxvolume_scripts
python3 digix_info_bot.py >> ../dgxvolume.markdown
cd ..

