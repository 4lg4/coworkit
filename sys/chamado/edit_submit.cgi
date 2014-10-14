#!/usr/bin/perl

$nacess = "10";
require "../cfg/init.pl";

$ID               = &get('ID');                # id testes de sessao
$COD              = &get('COD');               # codigo para edicao
$RECOD            = &get('RECOD');             # codigo do pai para reabertura de chamado 

# $usuario        = $USER->{usuario};        # usuario logado criador do chamado
# $usuario        = &get('responsavel');       # usuario logado criador do chamado
$cliente          = &get('cliente');		
$cliente_descrp   = &get('cliente_descrp');
$empresa_endereco = &get('empresa_endereco');  # endereco vinculado a empresa selecionada
$problema         = &get('descrp');            # problema / solicitacao feita pelo cliente
$prioridade       = &get('prioridade_radios'); # prioridade do chamado
$plano            = &get('plano_radios');      # planos do chamado
$area             = &get('area_radios');       # area do chamado
$data_previsao    = &get('data_previsao');     # prioridade do chamado
$data_previsao_descrp = &dateToShow($data_previsao);
$tempo_previsao   = &get('tempo_previsao');    # tempo previsto para a conclusao do chamado
$tempo_previsao_descrp = $tempo_previsao;
if($tempo_previsao_descrp eq "")
	{
	$tempo_previsao_descrp = "00:00";
	}
$solicitante      = &get('solicitante');       # solicitante do chamado

$usuario_executor = &get('executor');          # primeiro executor, usado somente na inclusao
@emails           = &get_array('emails_list_radios'); # lista de emails

# acoes do chamado
# v2 alpha 1
# @acao_codigo          = &get_array('acao_codigo');
# @acao_tempo           = &get_array('acao_tempo');
# @acao_tipo            = &get_array('acao_tipo');
# @acao_descrp          = &get_array('acao_descrp');
# @acao_executor        = &get_array('acao_executor');
# @acao_executor_descrp = &get_array('acao_executor_descrp');
# @acao_data_execucao   = &get_array('acao_data_execucao');
# @acao_sigiloso        = &get_array('acao_sigiloso');
# @acao_interno         = &get_array('acao_interno');
# @acao_empresa         = &get_array('acao_empresa');

$acao_new            = &get('acao_new');
$acao_tempo          = &get('acao_tempo_new');
$acao_tempo_descrp = $acao_tempo;
if($acao_tempo_descrp eq "")
	{
	$acao_tempo_descrp = "00:00";
	}
$acao_tipo           = &get('acao_tipo_new');
$acao_descrp_interno = &get('acao_descrp_interno_new');
$acao_descrp_publico = &get('acao_descrp_publico_new');
$acao_executor       = &get('acao_executor_new');
$acao_sigiloso       = &get('acao_sigiloso_new');
$acao_data           = &get('acao_data_new');
$acao_data_execucao  = &get('acao_data_execucao_new');

# headers
print $query->header({charset=>utf8});

# acao_executor_descrp

# lista emails se existir 
#$i=0;
#foreach $c (@acao_descrp) {
#    print " -> ".$c."<hr>";
#    $i+=1;
#}

# debug();
# exit;
# teste campos obrigatorios

# se for cliente do parceiro
#
if($USER->{tipo} eq "99") {
    if(!$empresa_endereco || !$problema || !$prioridade || !$area || !$solicitante) {
        new DDialog("verifique os campos obrigatórios","error",true); # gera dialogo de erro e para execucao
    }
} else {
    if(!$empresa_endereco || !$problema || !$prioridade || !$area || !$data_previsao || !$solicitante || !$tempo_previsao) {
        new DDialog("verifique os campos obrigatórios","error",true); # gera dialogo de erro e para execucao
    }
}

# normaliza variaveis para salvar no banco
if(!$data_previsao){
    $data_previsao = NULL;
} else {
    $data_previsao = "'".&dateToSave($data_previsao)."'";
}
if(!$tempo_previsao){
    $tempo_previsao = NULL;
} else {
    $tempo_previsao = "'$tempo_previsao'";
}
if(!$usuario_executor){ 
    $usuario_executor = NULL
}

# DEBUG
# lista emails se existir 
#foreach $email (@emails) {
#    print " -> ".$email."<hr>";
#}

# inicia SQls execs
$dbh->begin_work;


#  Statments

# V2 alpha 1
# desabilitado pois nao existem updates no modulo 
# if($COD ne ""){ # Update
#	require "./edit_submit_update.cgi";
# } else { # Insert
#	require "./edit_submit_insert.cgi";
# }


# insert
if(!$COD){ 
    
    require "./edit_submit_insert.cgi";
    $title = "coworkIT - Novo ticket ".$COD;
    
# update
} else { 
    
    require "./edit_submit_update.cgi";
    $title = "coworkIT - Atualização ticket ".$COD;
    
}

# debug();

# update / insert acoes
# $i     = 0;
# $acoes = "";

if($acao_new eq "1"){
# foreach $codigo (@acao_codigo) {
    # print " -> ".$adata." -> ".@acao_tempo[$i]." -> ".@acao_descrp[$i]." -> ".@acao_tipo[$i]." -> ".@acao_executor[$i]." -> ".@acao_data_execucao[$i]."<hr>";
    
 #   if(!$codigo){ # insert
 
        # ajusta variaveis
        $descrp          = $acao_descrp_interno;
        $tempo           = $acao_tempo;
        $sigiloso        = $acao_sigiloso;
        # $interno         = @acao_interno[$i];
        $executor        = $acao_executor;
        $executor_descrp = $acao_descrp_publico;
        $data_execucao   = $acao_data_execucao;
        $empresa         = $acao_empresa;
        $tipo            = $acao_tipo;
    
        if(!$data_execucao){
            $data_execucao = "now()";
        } else {
            $data_execucao = "'".&dateToSave($data_execucao)."'";
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
            $empresa = false;
        }
        if(!$tipo){
            $tipo = NULL;
        }
                
        # sql
        # V2 alpha 1   # $acoes .= "($USER->{usuario}, $tempo, '$descrp', $executor, $sigiloso, $interno, $tipo, $COD, '$executor_descrp', $data_execucao, $empresa),";
        # $acoes .= "($USER->{usuario}, $tempo, '$descrp', $executor, $sigiloso, $tipo, $COD, '$executor_descrp', $data_execucao, $empresa),";
        
        
        # new DDialog("insert into tkt_acao (usuario, tempo, descrp, executor, sigiloso, tipo, tkt, executor_descrp, data_execucao, empresa) values ($USER->{usuario}, $tempo, '$descrp', $executor, $sigiloso, $tipo, $COD, '$executor_descrp', $data_execucao, $empresa)");
        # exit;
        
        &DBE("insert into tkt_acao (
                    usuario, tempo, descrp, executor, sigiloso, tipo, 
                    tkt, executor_descrp, data_execucao, empresa
                ) values (
                    $USER->{usuario}, $tempo, '$descrp', $executor, $sigiloso, 
                    $tipo, $COD, '$executor_descrp', $data_execucao, $empresa
                )");
 #   }
    
#    $i += 1;
}

# insere novas acoes
# v2 alpha 1
# if($acoes){
#    $acoes = substr($acoes, 0,-1); # remove ultima virgula
#    # V2 alpha 1      # &DBE("insert into tkt_acao (usuario, tempo, descrp, executor, sigiloso, interno, tipo, tkt, executor_descrp, data_execucao, empresa) values $acoes");
#    &DBE("insert into tkt_acao (usuario, tempo, descrp, executor, sigiloso, tipo, tkt, executor_descrp, data_execucao, empresa) values $acoes");
# }



#
# Chamado Emails
#   ajusta lista de emails
#
&DBE("delete from tkt_email where tkt = $COD"); # remove todas as entradas antes de inserir
if(@emails > 0) {
	# gera sql
	foreach $email (@emails) {
		$email_list .= "($COD,'".$email."'),";
	}    
	# save	list
	$email_list = substr($email_list, 0,-1); # remove ultima virgula
	&DBE("insert into tkt_email (tkt, email) values $email_list");
}

#
#   emails dos usuarios que estao trabalhando no chamado
#
$DB = &DBE("
    select 
        *
    from 
        tkt_email_acao_full
    where 
        tkt = $COD
");

@emails_internos = ();
while($email = $DB->fetchrow_hashref) {
    if($email->{remetente}) {
        push(@emails_internos, $email->{remetente});
    }
    
    if($email->{destinatario}) {
	    push(@emails_internos, $email->{destinatario});
    }
}
@emails_internos = uniq(@emails_internos);

#
# Envia email comunicao
#
require "./edit_sendmail.cgi";


# finaliza SQLs
$dbh->commit;

print<<HTML;
<script>    
    eos.core.call.module.tkt($COD); // carrega modulo tkt
</script>
HTML
