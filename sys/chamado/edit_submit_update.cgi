#!/usr/bin/perl

$nacess = "10";
# require "../cfg/DPAC/DSendmail.pl";

# controle plano
if($plano) {
   $plano_ = " plano = $plano,";
}


# update chamado
DBE(
    "update  tkt set 
        $plano_ 
        data_previsao  = $data_previsao, 
        tempo_previsao = $tempo_previsao
    where
        codigo = $COD;
");




return true;


exit;


# V2 Alpha 1 
# update Chamado, desabilitado pois uma vez feito ja esta no cliente

# sql chamado
# $sql  = "update tkt set ";
# $sql .= "   usuario = $usuario, ";
# $sql .= "   empresa_endereco = $empresa_endereco, ";
# $sql .= "   usuario_executor = $usuario_executor, problema = '$problema', ";
# $sql .= "   prioridade = $prioridade, plano = $plano, area = $area,  ";
# $sql .= "   data_previsao = $data_previsao, solicitante = '$solicitante', tempo_previsao = $tempo_previsao ";
# $sql .= "where codigo = $COD ";

# &DBE($sql); # update chamado

# print "<hr>";
# print "<hr>";    

# update / insert acoes
$i     = 0;
$acoes = "";
foreach $codigo (@acao_codigo) {
    # print " -> ".$adata." -> ".@acao_tempo[$i]." -> ".@acao_descrp[$i]." -> ".@acao_tipo[$i]." -> ".@acao_executor[$i]." -> ".@acao_data_execucao[$i]."<hr>";
    
    # ajusta variaveis
    $descrp         = @acao_descrp[$i];
    $tempo          = @acao_tempo[$i];
    $sigiloso       = @acao_sigiloso[$i];
    $interno        = @acao_interno[$i];
    $executor       = @acao_executor[$i];
    $executo_descrp = @acao_executor_descrp[$i];
    $data_execucao  = @acao_data_execucao[$i];
    $empresa        = @acao_empresa[$i];
    $tipo           = @acao_tipo[$i];
    
    if(!$data_execucao){
        $data_execucao = NULL;
    } else {
        $data_execucao = "'$data_execucao'";
    }
    if(!$tempo){
        $tempo = NULL;
    } else {
        $tempo = "'$tempo'";
    }
    if(!$executor){
        $executor = NULL;
    }
    if(!$empresa){
        $empresa = NULL;
    }
    if(!$tipo){
        $tipo = NULL;
    }    
    
    if(!$codigo){ # insert
        $acoes .= "($USER->{usuario}, $tempo, '$descrp', $executor, $sigiloso, $interno, $tipo, $COD, '$executor_descrp', $data_execucao, $empresa),";
    } else { # update
        # salva somente o que pertencer ao usuario logado
        # if($USER->{usuario} eq @acao_executor[$i])
        # salva tudo
        # if($USER->{nacess} eq "s")
        
        print "<hr>";
        print "update tkt_acao set descrp='$descrp', sigiloso=$sigiloso, interno=$interno, executor=$executor, executor_descrp='$executor_descrp', data_execucao=$data_execucao, tempo=$tempo";
        
        # controla se pode fazer update e executa
        if($USER->{usuario} eq $executor || $USER->{tacess} eq "s"){
            &DBE("update tkt_acao set descrp='$descrp', sigiloso=$sigiloso, interno=$interno, executor=$executor, executor_descrp='$executor_descrp', data_execucao=$data_execucao, tempo=$tempo");
        }
    }
    
    $i += 1;
}
print "<hr>";
print "insert into tkt_acao (usuario, tempo, descrp, executor, sigiloso, interno, tipo, tkt, executor_descrp, data_execucao, empresa) values $acoes";
# exit;

# insere novas acoes
if($acoes){
    $acoes = substr($acoes, 0,-1); # remove ultima virgula
    &DBE("insert into tkt_acao (usuario, tempo, descrp, executor, sigiloso, interno, tipo, tkt, executor_descrp, data_execucao, empresa) values $acoes");
}

return true;
exit;

print "<hr> * $nacess -> $nacess_tipo";
foreach $k (keys %{ $USER }) {
    print "<hr>$k -> ".$USER->{$k};
}



