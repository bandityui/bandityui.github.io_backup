#!/usr/bin/gnuplot

# for GNUPLOT5.0
reset
set output "out.eps"
set term post eps color enh "Times-Bold" 26
set encoding utf8
#set grid

#set title "{/Symbol abcdefghijklmnopqrstuvwxyz   \245}"
#set ylabel "d^2{/Symbol s}/dp/d{/Symbol W} (mb/(MeV/c)/str)" 1,0
#set xlabel "K^+ Momentum (GeV/c)"

set multiplot layout 1,1 font ",18" \
margins 0.25,0.85,0.25,0.90 \
              spacing 0.00,0.00
#margins <left>,<right>,<bottom>,<top>

unset title
set grid
#set xrange [0 : 100 ]
show xrange
#set yrange [0 : 1000]
show yrange
set xlabel ""
set ylabel "Weekly on-chain volume (DGX)"
set mxtics 2
set xtics rotate
unset key
set mytics 2
set my2tics 2

set xdata time
set timefmt "%Y-%m-%d %H:$M"
set format x "%d/%m"

LW=4.0
p '< paste weekly_datetimes.dat weekly.dat' u 1:4 w lp pt 5 lw LW t "Weekly on-chain volume"

unset multiplot


