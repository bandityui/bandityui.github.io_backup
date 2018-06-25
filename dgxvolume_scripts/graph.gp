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
margins 0.25,0.85,0.35,0.90 \
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
set mxtics 2
set xtics rotate
set key bottom right
set ytics 0,100,10000 nomirror tc lt 1
set mytics 2

set y2tics 0,2,100 nomirror tc lt 2
set my2tics 2

stats "24hr_volume.dat" u 1:4 nooutput
set y2range [0:1.5*STATS_max_y]
set y2label "Percent of total supply" offset -2,0

stats "24hr_volume.dat" u 1:3 nooutput
set yrange [0.96*STATS_min_y:1.04*STATS_max_y]

set xdata time
set timefmt "%Y-%m-%d %H:$M"
set format x "%d/%m %H:%M"

LW=4.0
p '24hr_volume.dat' u 1:3 w lp pt 5 lw LW t "24 hr on-chain volume",\
  '' u 1:4 w lp pt 4 lw LW axes x1y2 t "Percent of total supply"

unset multiplot

