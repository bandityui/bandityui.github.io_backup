#!/usr/bin/gnuplot

# for GNUPLOT5.0
reset
set output "fees.eps"
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
set ylabel "Total Fees Collected (DGX)"
set mxtics 2
set mytics 2
set xtics rotate
unset key

set xdata time
set timefmt "%Y-%m-%d %H:$M"
set format x "%d/%m/%Y"
set xrange ["2018-03-22 00:00" :]

LW=3.0

p '86400.dat' u 1:($5/1e9) w l lt 6 lw LW 

unset multiplot

