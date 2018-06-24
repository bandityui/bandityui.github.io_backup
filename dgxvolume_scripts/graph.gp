#!/usr/bin/gnuplot

# for GNUPLOT5.0
reset
set output "out.eps"
set term post eps color enh "Times-Bold" 28
set encoding utf8
#set grid

#set title "{/Symbol abcdefghijklmnopqrstuvwxyz   \245}"
#set ylabel "d^2{/Symbol s}/dp/d{/Symbol W} (mb/(MeV/c)/str)" 1,0
#set xlabel "K^+ Momentum (GeV/c)"

set multiplot layout 1,1 font ",18" \
margins 0.25,0.85,0.29,0.90 \
              spacing 0.00,0.00
#margins <left>,<right>,<bottom>,<top>

unset title
set grid
#set xrange [0 : 100 ]
show xrange
#set yrange [0 : 1000]
show yrange
set xlabel "Time (hrs)"
set ylabel "24 hr on-chain volume (DGX)"
set mytics 2
set mxtics 2
set xtics rotate 

set xdata time
set timefmt "%Y-%m-%d"
#set format x "%d/%m/%Y"
p '24hr_volume.dat' u 1:2 w lp pt 5 lw 4.0 t "24 hr on-chain volume"

unset multiplot

