#!/usr/bin/perl

# edit_acoes.cgi
#
# Acoes, lista acoes do banco
# 

$nacess = "10";
require "../cfg/init.pl";

$ID = &get('ID');
$COD = &get('COD');


$DB = DBE("select ta.*, u.nome as usuario_nome, tt.descrp as tipo_descrp, ue.usuario as executor, ue.nome as executor_nome  from tkt_acao as ta left join usuario as u on u.usuario = ta.usuario left join usuario as ue on ue.usuario = ta.executor left join tkt_acao_tipo as tt on tt.codigo = ta.tipo where ta.tkt = $COD order by ta.data asc");
while($ta = $DB->fetchrow_hashref)
	{
	$ta->{data} = dateToShow($ta->{data});
    $ta->{data_execucao} = dateToShow($ta->{data_execucao});
	
    # ajusta campos
    if($ta->{sigiloso} == 0){
        $ta->{sigiloso} = false;
    } else {
        $ta->{sigiloso} = true;
    }
    
    if($ta->{interno} == 0){
        $ta->{interno} = false;
    } else {
        $ta->{interno} = true;
    }
    
    $ta->{descrp} = &get($ta->{descrp}, "HTML");
    $ta->{executor_descrp} = &get($ta->{executor_descrp}, "HTML");
    
    
    #
    #   Cliente do parceiro
    #
    if($USER->{tipo} eq "99") {
        $ta->{descrp} = "";
    }
    
    $RJ .= "    {";
    $RJ .= "    codigo   : $ta->{codigo},";
    $RJ .= "    data     : '$ta->{data}',";
#    $RJ .= "    data     : '$ta->{data_execucao}',";
    $RJ .= "    sigiloso : $ta->{sigiloso},";
    $RJ .= "    interno  : $ta->{interno},";
    $RJ .= "    data_execucao : '$ta->{data_execucao}',";
    $RJ .= "    usuario  : { ";
    $RJ .= "        usuario  : '$ta->{usuario}',";
    $RJ .= "        nome     : '$ta->{usuario_nome}',";
    $RJ .= "        descrp   : '$ta->{descrp}'";
    $RJ .= "    },";
    $RJ .= "    executor     : { ";
    $RJ .= "        executor : '$ta->{executor}',";
    $RJ .= "        nome     : '$ta->{executor_nome}',";
    $RJ .= "        descrp   : '$ta->{executor_descrp}'";
    $RJ .= "    },";
    $RJ .= "    tipo     : { ";
    $RJ .= "        tipo   : '$ta->{tipo}',";
    $RJ .= "        descrp : '$ta->{tipo_descrp}'";
    $RJ .= "    },";
    $RJ .= "    tempo    : '$ta->{tempo}',";
    $RJ .= "    anexos   : [";
    $RJ .= "        { codigo : 1, descrp : 'anexo 1' },";
    $RJ .= "        { codigo : 2, descrp : 'anexo 2' },";
    $RJ .= "        { codigo : 12, descrp : 'anexo 23' },";
    $RJ .= "    ]},";
	}

# print $query->header('application/json; charset=utf-8');
# print $RJ;

print $query->header({charset=>utf8});
print<<HTML;
    <script>
 	    chamado.acoes.list([$RJ]);
    </script>
HTML
