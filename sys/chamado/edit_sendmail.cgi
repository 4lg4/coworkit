#!/usr/bin/perl


require "../cfg/DPAC/DSendmail.pl";

	# Inicio da rotina de envio de e-mails
	
	# Campos adicionais para o envio de e-mail
    
    # endereco da empresa
	$DB2 = &DBE("select * from empresa_endereco where codigo = '$empresa_endereco' ");
	while($enderecos = $DB2->fetchrow_hashref) {
        
		$empresa_endereco_descrp = $enderecos->{endereco};
		if(!$enderecos->{complemento} ) {
			$empresa_endereco_descrp .= ", ".$enderecos->{complemento};
		}
		if(!$enderecos->{bairro}) {
			$empresa_endereco_descrp .= " - ".$enderecos->{bairro};
		}
		if(!$enderecos->{cidade} || !$enderecos->{uf}) {
			$empresa_endereco_descrp .= " - ".$enderecos->{cidade};
		}
		if($enderecos->{uf} =~ /[a-z]/i){
			if(!$enderecos->{cidade}){
				$empresa_endereco_descrp .= "/";
			}
			$empresa_endereco_descrp .= $enderecos->{uf};
		}
	}
    
    # area da empresa
	$DB2 = &DBE("select * from empresa_area_tipo where codigo = '$area' ");
	while($areas = $DB2->fetchrow_hashref) {
		$area_descrp = $areas->{descrp};
	}
    
    # plano da empresa
	$DB2 = &DBE("select * from prod_servicos where codigo = '$plano' ");
	while($planos = $DB2->fetchrow_hashref) {
		$plano_descrp = $planos->{descrp};
	}
    
    # prioridade do ticket
	$DB2 = &DBE("select * from tkt_prioridade where codigo = '$prioridade' ");
	while($p = $DB2->fetchrow_hashref) {
		$prioridade_descrp = $p->{descrp};
	}
    
    # dados do ticket
	$DB2 = &DBE("select * from tkt where codigo = '$COD' ");
	while($d = $DB2->fetchrow_hashref) {
		$data_cad = &dateToShow($d->{data});
	}
    
    # tipo de acao
	if($acao_tipo) {
		$DB2 = &DBE("select * from tkt_acao_tipo where codigo = '$acao_tipo' ");
		while($a = $DB2->fetchrow_hashref) {
			$acao_tipo_descrp = $a->{descrp};
		}
	}
    
    # executor
	if($acao_executor) {
		$DB2 = &DBE("select * from usuario where usuario = '$acao_executor' ");
		while($a = $DB2->fetchrow_hashref) {
			$acao_executor_descrp = $a->{nome};
		}
	} else {
		$acao_executor_descrp = "";
	}
    
		
# Cabeçalho do e-mail
$message=<<END;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
</head>
<body style="margin: 0px; padding: 0px; font: 16px/26px Helvetica, Helvetica Neue, Arial; color: #777">
<div style="height: 25px; background-color: #FF9700; border-bottom: 10px solid #31517b;">
	<img class="logo" src="cid:coworkIT.png" width="120" height="110" style="position: relative; top: -35px; left: 20px;">
</div>

END

# Conteudo do e-mail
if($title =~ /Novo/) {
    
$message.=<<END;
<div style="margin: 40px 120px;">
<p style="font-size: 1.5em">Informamos o cadastramento do novo ticket no sistema coworkIT, por $USER->{nome}, com o c&oacute;digo <b>$COD</b>:</p>

<table width=100% cellpadding=0 cellspacing=0>
<tr>
    <td style="width: 150px; vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Data prevista:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$data_previsao_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Tempo previsto:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$tempo_previsao_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Solicitante:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$solicitante</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Descri&ccedil;&atilde;o:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;"><div style="min-height: 100px">$problema</div></td>
</tr>
<tr><td colspan=2>&nbsp;</td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Empresa:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$cliente_descrp ($cliente)</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Endere&ccedil;o:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$empresa_endereco_descrp</td>
</tr>
<tr><td colspan=2>&nbsp;</td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">&Aacute;rea:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$area_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Plano:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$plano_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Prioridade:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$prioridade_descrp</td>
</tr>
</table>

</div>

</body>
</html>   
END


# Novo andamento, acoes
} else {
		
    if($acao_new eq "1") {
        
        # se usuario nao for executor
        if($USER->{usuario} ne $acao_executor) {
            
$message.=<<END;
<div style="margin: 40px 120px;">
<p style="font-size: 1.5em">Informamos o cadastramento de novo encaminhamento no sistema CoworkIT, referente ao ticket <b>$COD</b>:</p>
<table width=100% cellpadding=0 cellspacing=0>
<tr>
    <td style="width: 150px; vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Data:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$acao_data_execucao</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">De:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$USER->{nome}</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Para:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$acao_executor_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Mensagem:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;"><div style="min-height: 100px">$acao_descrp_publico</div></td>
</tr>
<tr><td colspan=2>&nbsp;</td></tr>
END

        # se usuario for executor 
        } else {
            
$message.=<<END;
<div style="margin: 40px 120px;">
<p style="font-size: 1.5em">Informamos o cadastramento de novo andamento no sistema CoworkIT, referente ao ticket <b>$COD</b>:</p>
<table width=100% cellpadding=0 cellspacing=0>
<tr>
    <td style="width: 150px; vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Data execução:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$acao_data_execucao</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Tempo gasto:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$acao_tempo_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Executor:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$acao_executor_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Tipo Atend.:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$acao_tipo_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Servi&ccedil;o realizado:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;"><div style="min-height: 100px">$acao_descrp_publico</div></td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Cadastrado por:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$USER->{nome}</td>
</tr>
<tr><td colspan=2>&nbsp;</td></tr>
END

        }        
    } else {
            
            
$message.=<<END;
<div style="margin: 40px 120px;">
<p style="font-size: 1.5em">Informamos a atualização do ticket <b>$COD</b> do sistema CoworkIT:</p>
<table width=100% cellpadding=0 cellspacing=0>
END

	}
    
$message.=<<END;
<tr>
    <td style="width: 150px; vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Data prevista:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$data_previsao_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Tempo previsto:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$tempo_previsao_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Solicitante:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$solicitante</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Descri&ccedil;&atilde;o:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;"><div style="min-height: 100px">$problema</div></td>
</tr>
END

	if($acao_new ne "1") {
$message.=<<END;
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Cadastrado por:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$USER->{nome} em $data_cad</td>
</tr>
END
	}
        
$message.=<<END;
<tr><td colspan=2>&nbsp;</td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Empresa:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$cliente_descrp ($cliente)</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Endere&ccedil;o:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$empresa_endereco_descrp</td>
</tr>
<tr><td colspan=2>&nbsp;</td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">&Aacute;rea:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$area_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Plano:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$plano_descrp</td>
</tr>
<tr><td colspan=2 style="height: 2px"></td></tr>
<tr>
    <td style="vertical-align: top; background-color: #3167b3; color: #fff; font-weight: bold; padding: 6px 4px;">Prioridade:</td>
    <td style="padding: 4px 8px; border: solid 1px #3167b3; font-weight: bold;">$prioridade_descrp</td>
</tr>
</table>

</div>

</body>
</html>   
END
}

# envia email
# 	if($acao_sigiloso eq "false") {
        
		# Envia e-mail
        # print join(" ", @emails_internos), "\n\n";
        push(@emails, @emails_internos);
        @emails = uniq(@emails);
        # print join(" ", @emails_internos), "\n\n";
        # exit;
		if(sendmail(\@emails, $title, $message)) {
			if($logmail ne "") {
				&DBE("insert into tkt_email_historico (tkt, email_historico) values ('$COD', '$logmail') ");
			}
		} else {
			print "<script> alerta('Não foi possível enviar e-mail!');</script>";
			exit;
	    }		
        # }


return true;
