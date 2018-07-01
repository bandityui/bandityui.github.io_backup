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

set ytics 0,200,900000 nomirror tc lt 1
set mytics 2

set y2tics 0,2,100 nomirror tc lt 2
set my2tics 2

stats "weekly.dat" u 1:4 nooutput
set y2range [0:1.5*STATS_max_y]
set y2label "Percent of total supply" offset -1,0

stats "weekly.dat" u 1:3 nooutput
set yrange [0.9*STATS_min_y:1.04*STATS_max_y]

set xdata time
set timefmt "%Y-%m-%d %H:$M"
set format x "%d/%m"

LW=4.0
p 'weekly.dat' u 1:3 w lp pt 5 lw LW t "Weekly on-chain volume",\
  '' u 1:(100*$3/$4) w lp pt 3 lw LW axes x1y2 t "Percent of total supply"

unset multiplot

