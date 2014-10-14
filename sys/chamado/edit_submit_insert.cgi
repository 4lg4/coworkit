#!/usr/bin/perl

$nacess = "10";
# require "../cfg/DPAC/DSendmail.pl";

# sql chamado V2 alpha 1
# $sql .= "   usuario, empresa_endereco, usuario_executor, problema, "; # V2 alpha 1
# $sql .= "   $USER->{usuario}, $empresa_endereco, $usuario_executor, '$problema', "; # V2 alpha 1

#
#   cliente do parceiro
#
if($USER->{tipo} eq "99") {
    $DB = DBE("
        select 
            * 
        from 
            parceiro_empresa 
        where 
            empresa = $USER->{empresa}
    ");
    
    if($DB->rows() > 0){
        $p = $DB->fetchrow_hashref;
        $parceiro = $p->{parceiro};
    }
} else {
    $parceiro = $USER->{empresa};
}

# controle plano
if(!$plano) {
   $plano  = NULL;
}

# se for reabertura de chamado
if(!$RECOD){
    $RECOD = NULL;
} else {
    $data_previsao = NULL;
    $tempo_previsao = NULL;
}


# insere novo chamado 
$COD = &DBE(
    "insert into tkt ( 
        usuario, empresa_logada, empresa_endereco, problema, prioridade, 
        plano, area, data_previsao, solicitante, tempo_previsao, pai
    ) values (
        $USER->{usuario}, $parceiro, $empresa_endereco, '$problema', $prioridade, 
        $plano, $area, $data_previsao, '$solicitante', $tempo_previsao, $RECOD 
    )"
);


# recupera codigo inserido
# $DB = &DBE("select currval('tkt_codigo_seq')");
# $row = $DB->fetch;
# $COD = @$row[0];

# V2 alpha 1 
# desabilitado pois o conceito mudou um pouco
# usuario executor
#   insere primeiro lancamento somente com o executor
# if($usuario_executor){
#     &DBE("insert into tkt_acao (tkt, usuario, executor) values ($COD, $USER->{usuario}, $usuario_executor)");
# }

return true;

