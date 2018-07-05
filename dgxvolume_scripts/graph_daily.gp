#!/usr/bin/gnuplot

# for GNUPLOT5.0
reset
set output "daily.eps"
set term post eps color enh "Times-Bold" 22
set encoding utf8
#set grid

#set title "{/Symbol abcdefghijklmnopqrstuvwxyz   \245}"
#set ylabel "d^2{/Symbol s}/dp/d{/Symbol W} (mb/(MeV/c)/str)" 1,0
#set xlabel "K^+ Momentum (GeV/c)"

set multiplot layout 1,1 font ",18" \
margins 0.25,0.75,0.25,0.90 \
              spacing 0.00,0.00
#margins <left>,<right>,<bottom>,<top>

unset title
set grid
#set xrange [0 : 100 ]
show xrange
#set yrange [0 : 1000]
show yrange
set xlabel ""
set ylabel "Daily on-chain volume (DGX)"
set mxtics 2
set xtics rotate
unset key

set ytics 0,100,10000000 nomirror tc lt 1
set mytics 2

set y2tics 0,10000,10000000 nomirror tc lt 2
set my2tics 2

stats "daily.dat" u 1:4 nooutput
set y2range [0:1.1*STATS_max_y]
set y2label "Total supply (DGX)" offset -1,0

stats "daily.dat" u 1:3 nooutput
set yrange [0.9*STATS_min_y:1.05*STATS_max_y]

set xdata time
set timefmt "%Y-%m-%d %H:$M"
set format x "%d/%m/%Y"

LW=4.0
p 'daily.dat' u 1:3 w l lt 1 lw LW t "Daily on-chain volume",\
  '' u 1:4 w l lt 2 lw LW axes x1y2 t "Total supply"

unset multiplot

