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
margins 0.25,0.75,0.25,0.80 \
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
set key tmargin maxcolumns 2 maxrows 3 
#unset key

set ytics 0,1000,10000000 nomirror tc lt 6
set mytics 2

set y2tics 0,10000,10000000 nomirror tc lt 7
set my2tics 2

stats "86400.dat" u 1:4 nooutput
set y2range [0:1.1*STATS_max_y/1e9]
set y2label "Total supply (DGX)" offset -1,0

stats "86400.dat" u 1:3 nooutput
set yrange [0.9*STATS_min_y/1e9:1.05*STATS_max_y/1e9]

set xdata time
set timefmt "%Y-%m-%d %H:$M"
set format x "%d/%m/%Y"
set xrange ["2018-03-22 00:00" :]

LW=3.0

binwidth = 5
bin(t) = (t - (int(t) % binwidth))
set boxwidth 0.9 relative
set style fill solid 1.0

p '86400.dat' u 1:(bin($3)/1e9) lt 6 lw LW smooth freq with boxes t "Other",\
  '' u 1:(bin($6+$7+$8+$9)/1e9) lt 1 lw LW smooth freq with boxes t "to Kryptono",\
  '' u 1:(bin($6+$7+$8)/1e9) lt 3 lw LW smooth freq with boxes t "from Kyber",\
  '' u 1:(bin($6+$7)/1e9) lt 2 lw LW smooth freq with boxes t "to Kyber",\
  '' u 1:(bin($6)/1e9) lt 4 lw LW smooth freq with boxes t "from Digix",\
  '' u 1:($4/1e9) w l lt 7 lw LW axes x1y2 t "Total Supply"

unset multiplot

