#!/usr/bin/perl

$nacess = "76";
require "../cfg/init.pl";

# vars
$ID  = &get('ID');
$COD = &get('COD');

# statment
$DB = DBE("
    select 
        *
    from 
        prod_mercadorias_full
    where
        codigo   = $COD and
        parceiro = $USER->{empresa}
");

# plano
$produto = $DB->fetchrow_hashref;

if($produto->{preco_custo} !~ /\./){
    $produto->{preco_custo} .= ".00";
} elsif($produto->{preco_custo} =~ /\.\d{1}$/){ 
    $produto->{preco_custo} .= "0";
}

if($produto->{preco_venda} !~ /\./){
    $produto->{preco_venda} .= ".00";
} elsif($produto->{preco_venda} =~ /\.\d{1}$/){ 
    $produto->{preco_venda} .= "0"; 
}


# print
print $query->header({charset=>utf8});

    $R  = '{ ';
    $R .= '     "descrp"      : "'.$produto->{descrp}.'",  ';
    $R .= '     "status"      : "'.$produto->{status}.'",  ';
    $R .= '     "modelo"      : "'.$produto->{modelo}.'",  ';
    $R .= '     "unidade"     : "'.$produto->{unidade}.'",  ';
    $R .= '     "marca"       : { ';
    $R .= '         "id"  : "'.$produto->{marca}.'",  ';
    $R .= '         "val" : "'.$produto->{marca_descrp}.'"  ';
    $R .= '     }, ';
    $R .= '     "partnumber"  : "'.$produto->{partnumber}.'",  ';
    $R .= '     "link"        : "'.$produto->{link}.'",  ';
    $R .= '     "obs"         : "'.$produto->{obs}.'",  ';
    $R .= '     "preco_custo" : "'.$produto->{preco_custo}.'",  ';
    $R .= '     "preco_venda" : "'.$produto->{preco_venda}.'"  ';
    $R .= '}  ';

print $R;
