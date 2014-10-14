#!/usr/bin/perl

require "../../cfg/init.pl";
$SHOW = &get('SHOW');
$PESQ = &get('PESQ');
$CAMPO = &get('CAMPO');
$ORDER = &get('ORDER');
$PESQLETRA = &get('PESQLETRA');
$INI = &get('INI');
if($INI eq "")
	{
	$INI = 0;
	}
$MAX = 150;
$NREG = 0;


#print $query->header({charset=>utf8});
print "Content-type: text/plain; charset=UTF-8\n\n";

if(-e "./$SHOW.pl")
	{
	require "./$SHOW.pl";
	}
else
	{
	require "./default.pl";
	}


if($NREG == 0)
	{
	$NREG = $rv;
	}
#$LREG = $NREG-$MAX;
$PAG = int((($INI+1)/$MAX)+1);
$TPAG = int(($NREG/$MAX)+1);
$LREG = int(($TPAG-1)*$MAX);

if($INI == 0 && $NREG <= $MAX)
	{
	# não tem registros suficientes para paginar
print<<HTML;
<div id='nav' style='float: right'><span id='limits'></span><img src='$dir{'img_syscall'}grid/first_disabled.png' border=0 style='margin: 2px;'><img src='$dir{'img_syscall'}grid/rew_disabled.png' border=0 style='margin: 2px'> <span style='position: relative;'>Total de $NREG registros: Página $PAG de $TPAG</span> <img src='$dir{'img_syscall'}grid/fwd_disabled.png' border=0 style='margin: 2px'><img src='$dir{'img_syscall'}grid/last_disabled.png' border=0 style='margin: 2px'></div><br>
HTML
	}
elsif($INI == 0 && $NREG > $MAX)
	{
	# Primeira página
print<<HTML;
<div id='nav'><div id='limits'></div><img src='$dir{'img_syscall'}grid/first_disabled.png' border=0 style='margin: 2px;'><img src='$dir{'img_syscall'}grid/rew_disabled.png' border=0 style='margin: 2px'> <span style='position: relative;'>Total de $NREG registros: Página $PAG de $TPAG</span> <a href='javascript:goto($INI+$MAX)'><img src='$dir{'img_syscall'}grid/fwd.png' border=0 style='margin: 2px'></a><a href='javascript:goto($LREG)'><img src='$dir{'img_syscall'}grid/last.png' border=0 style='margin: 2px'></a></div><br>
HTML
	}
elsif($INI > 0 && $NREG > $INI+$MAX)
	{
	# Páginas intermediárias
print<<HTML;
<div id='nav'><div id='limits'></div><a href='javascript:goto(0)'><img src='$dir{'img_syscall'}grid/first.png' border=0 style='margin: 2px;'></a><a href='javascript:goto($INI-$MAX)'><img src='$dir{'img_syscall'}grid/rew.png' border=0 style='margin: 2px'></a> <span style='position: relative;'>Total de $NREG registros: Página $PAG de $TPAG</span> <a href='javascript:goto($INI+$MAX)'><img src='$dir{'img_syscall'}grid/fwd.png' border=0 style='margin: 2px'></a><a href='javascript:goto($LREG)'><img src='$dir{'img_syscall'}grid/last.png' border=0 style='margin: 2px'></a></div><br>
HTML
	}
elsif($INI >= $LREG)
	{
	# Última Página
print<<HTML;
<div id='nav'><div id='limits'></div><a href='javascript:goto(0)'><img src='$dir{'img_syscall'}grid/first.png' border=0 style='margin: 2px;'></a><a href='javascript:goto($INI-$MAX)'><img src='$dir{'img_syscall'}grid/rew.png' border=0 style='margin: 2px'></a> <span style='position: relative;'>Total de $NREG registros: Página $PAG de $TPAG</span> <img src='$dir{'img_syscall'}grid/fwd_disabled.png' border=0 style='margin: 2px'><img src='$dir{'img_syscall'}grid/last_disabled.png' border=0 style='margin: 2px'></div><br>
HTML
	}
else
	{
print<<HTML;
<div id='nav' style='float: right'><div id='limits'></div><img src='$dir{'img_syscall'}grid/first_disabled.png' border=0 style='margin: 2px;'><img src='$dir{'img_syscall'}grid/rew_disabled.png' border=0 style='margin: 2px'> <span style='position: relative;'>Total de $NREG registros: Página $PAG de $TPAG</span> <img src='$dir{'img_syscall'}grid/fwd_disabled.png' border=0 style='margin: 2px'><img src='$dir{'img_syscall'}grid/last_disabled.png' border=0 style='margin: 2px'></div><br>
HTML
	}
    


# adiciona limites se for empresas    
if($SHOW eq "empresas") {
print<<HTML;
    <script>
        // atualiza limites
        top.eos.core.limit.empresa.get(function(x){
            \$("#limits").html(x);
        });
    </script>
HTML
}


