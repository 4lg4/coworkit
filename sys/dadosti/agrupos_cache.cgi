#!/usr/bin/perl

$nacess = '204';
require "../cfg/init.pl";

$ID = &get('ID');

$DB = DBE("
    select 
    	a.*
    from 
    	parceiro_agrupo as pa 
    join
    	agrupo as a on a.codigo = pa.agrupo
    where
    	pa.parceiro = $USER->{empresa}
    order by 
        a.descrp
    asc
");

if($DB > 0) {
	while($a = $DB->fetchrow_hashref) {
    	$R .= "{";
        $R .= "  \"codigo\" : \"$a->{codigo}\", ";
        $R .= "  \"val\"    : \"$a->{codigo}\", ";
    	$R .= "  \"descrp\" : \"$a->{descrp}\" ";
        $R .= "},";
    }
    $R = "[".substr($R, 0,-1)."]";
}

print $query->header('application/json; charset="utf-8"');
print $R;



