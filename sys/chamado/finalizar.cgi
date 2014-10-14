#!/usr/bin/perl

$nacess = "10";
require "../cfg/init.pl";

# get vars
$ID  = &get('ID');


$COD      = &get('COD');
$cancelar = &get('cancelar');


print $query->header({charset=>utf8});

# cancela chamado
if($cancelar) {
    $cancelado  = "cancelado = true, ";
    $cancelado .= "cancelado_motivo = '$cancelar', ";
    $cancelado .= "cancelado_usuario = ".$USER->{usuario}.", ";
}

# atualiza tbl
&DBE("
    update tkt set
        $cancelado  
        finalizado = now()
    where codigo = $COD
"); 

# redireciona para o dashboard apos finalizar chamado
print<<HTML;
<script>
    eos.core.call.module.dashboard();
</script>
HTML


