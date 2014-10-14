#!/usr/bin/perl

$nacess = '204';
require "../cfg/init.pl";

$ID = &get('ID');

$DB = DBE("
    select 
        distinct g.codigo,
    	g.descrp
    from 
    	parceiro_grupo as pg 
    join
    	grupo as g on g.codigo = pg.grupo
	left join
    	agrupo_grupo as ag on ag.grupo = g.codigo
    where
    	pg.parceiro = $USER->{empresa} 
    order by 
        g.descrp
    asc
");

if($DB > 0) {
	while($g = $DB->fetchrow_hashref) {
    	$R .= "{";
        $R .= "  \"codigo\" : \"$g->{codigo}\", ";
        $R .= "  \"val\"    : \"$g->{codigo}\", ";
    	$R .= "  \"descrp\" : \"$g->{descrp}\" ";
        $R .= "},";
    }
    $R = "[".substr($R, 0,-1)."]";
}

print $query->header('application/json; charset="utf-8"');
print $R;



