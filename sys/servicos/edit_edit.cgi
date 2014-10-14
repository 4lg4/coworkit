#!/usr/bin/perl

$nacess = "51";
require "../cfg/init.pl";

# vars
$ID  = &get('ID');
$COD = &get('COD');

# statment
$DB = DBE("
    select 
        *
    from 
        prod_serv
    where
        codigo = $COD
");

# plano
$plano = $DB->fetchrow_hashref;

if($plano->{valor} !~ /\./){
    $plano->{valor} .= ".00";
} elsif($plano->{valor} =~ /\.\d{1}$/){ 
    $plano->{valor} .= "0";
}

# print
print $query->header({charset=>utf8});

    $R  = '{ ';
    $R .= '     "descrp"   : "'.$plano->{descrp}.'",  ';
    $R .= '     "status"   : "'.$plano->{status}.'",  ';
    $R .= '     "valor"    : "'.$plano->{valor}.'"  ';
    $R .= '}  ';

print $R;
