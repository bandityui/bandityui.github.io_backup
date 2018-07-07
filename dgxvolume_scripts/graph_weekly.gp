#!/usr/bin/gnuplot

# for GNUPLOT5.0
reset
set output "out.eps"
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
set ylabel "Weekly on-chain volume (DGX)" offset 1,0
set mxtics 2
set xtics rotate
unset key

set ytics 0,5000,10000000 nomirror tc lt 6
set mytics 2

set y2tics 0,10000,10000000 nomirror tc lt 7
set my2tics 2

stats "weekly.dat" u 1:5 nooutput
set y2range [0:1.1*STATS_max_y]
set y2label "Total supply (DGX)" offset -1.5,0

stats "weekly.dat" u 1:4 nooutput
set yrange [0.9*STATS_min_y:1.05*STATS_max_y]

set xdata time
set timefmt "%Y-%m-%d %H:$M"
set format x "%d/%m/%Y"
set xrange ["2018-03-22 00:00" :]

LW=3.0

binwidth = 5
bin(t) = (t - (int(t) % binwidth))
set boxwidth 7e4*binwidth absolute

p 'weekly.dat' u 1:(bin($3+$4)) lt 6 lw LW smooth freq with boxes,\
  '' u 1:5 w l lt 7 lw LW axes x1y2

#p 'weekly.dat' u 1:3 w lp pt 5 lw LW t "Weekly on-chain volume",\
  #'' u 1:4 w lp pt 3 lw LW axes x1y2 t "Total supply"

unset multiplot


