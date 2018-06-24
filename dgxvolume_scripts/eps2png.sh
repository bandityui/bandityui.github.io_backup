#!/bin/bash

convert -density 300 $1 tmp.png 
convert -flatten tmp.png ${1%.*}.png
rm tmp.png
#convert -flatten tmp.png tmp2.png
#convert -trim tmp2.png ${1%.*}.png 
#rm tmp.png tmp2.png

