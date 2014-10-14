#!/usr/bin/perl


if($ENV{'HTTPS'} eq "on")
	{
	$lnkdown = "https://";
	}
else
	{
	$lnkdown = "http://";
	}
$lnkdown .= $ENV{'SERVER_NAME'};
$lnkdown .= "/sys/upload/download.cgi?MD5="; 

# Dados do usuário
if($COD ne "")
	{
	$DB = &DBE("
		select p.codigo AS proc_codigo, p.titulo AS proc_titulo, p.descrp AS proc_descrp, p.endereco AS endereco_codigo, 
		ee.endereco AS proc_endereco, ee.cidade AS proc_cidade, ee.uf AS proc_uf, e.nome AS empresa_nome, e.codigo AS empresa_codigo from procedimentos AS p
		left join empresa_endereco AS ee on ee.codigo=p.endereco left join empresa AS e on e.codigo=p.empresa
		where p.codigo=$COD
		");
	while($proc=$DB->fetchrow_hashref)
		{
		$empresa_cod=$proc->{empresa_codigo};
		$endereco_cod=$proc->{endereco_codigo};
		$empresa=$proc->{empresa_nome};
		$endereco=$proc->{proc_endereco};
		if($proc->{proc_cidade} ne "" || $proc->{proc_uf} ne "")
			{
			$endereco.=" - ".$proc->{proc_cidade};
			}
		if($proc->{proc_uf} ne "")
			{
			if($proc->{proc_cidade} ne "")
				{
				$endereco.="/";
				}
			$endereco.=$proc->{proc_uf};
			}
		
		$titulo=$proc->{proc_titulo};
		$procedimento=$proc->{proc_descrp};
		}
		
	# Lista de TAGs do procedimento
	$DB = DBE("select procedimentos_tags.tag as tag_codigo, procedimentos_tags_tipo.descrp as tag_descrp from procedimentos_tags join procedimentos_tags_tipo on procedimentos_tags.tag = procedimentos_tags_tipo.codigo where procedimentos_tags.procedimento = '$COD' order by procedimentos_tags.ordem");
	$tags_list = "";
	$tags_wlist = "";
	while($t = $DB->fetchrow_hashref)
		{
		$tags_list .= "{val:'$t->{tag_descrp}',descrp:'$t->{tag_descrp}'},";
		$tags_wlist .= $t->{tag_descrp}.", ";
		}
	$tags_wlist =~ s/\,\s$//;
	
	if($ENV{'SCRIPT_NAME'} =~ /edit.cgi$/)
		{
		&get_end();
		}

	$DB = &DBE("select arquivo.* from arquivo join procedimentos_arquivo on arquivo.codigo = procedimentos_arquivo.arquivo where procedimentos_arquivo.procedimentos='$COD' order by arquivo.nome");
	$arq_list = "";
	while($arq=$DB->fetchrow_hashref)
		{
		$arq_nome[$n] = "- <a href='$lnkdown".$arq->{md5}."' target='_blank'>".$arq->{nome}."</a>";
		if($arq->{descrp} ne "")
			{
			$arq_list .= "{";
			$arq_list .= "val : $arq->{codigo},";
			$arq_list .= "descrp : '$arq->{descrp}',";
			$arq_list .= "type   : '".(&get($arq->{tipo},"NEWLINE_SHOW"))."',";
			$arq_list .= "size   : '$arq->{tamanho},'";
			$arq_list .= "},";
			$arq_nome[$n] .= " (".$arq->{descrp}.")";
			}
		$arq_nome[$n] .= " em ".&dateToShow($arq->{data});
		$n++;
		}
	}
else
	{
	$empresa_cod = &get('empresa');
	&get_end();
	}

sub get_end
	{
	if($empresa_cod ne "")
		{
		#Pega os endereços da empresa
		$DB2 = &DBE("select * from empresa_endereco where empresa = '$empresa_cod' order by codigo");
		
		#Verifica se existem
		if($DB2->rows()>0)
			{
			#Se existir ele puxa todos
			while($enderecos = $DB2->fetchrow_hashref)
				{
				#Insero no formulario de inclusão os endereços da empresa
				$endereco_descrp .="<div id=\"endereco_$enderecos->{codigo}\"> <input type=\"radio\" id=\"endereco\" name=\"cliente_endereco_radios\" value=\"$enderecos->{codigo}\"";
				if($enderecos->{codigo} eq $endereco_cod)
					{
					$endereco_descrp .= "checked";
					}
				$endereco_descrp .= "> ".$enderecos->{endereco};
				if($enderecos->{cidade} ne "" || $enderecos->{uf} ne "")
					{
					$endereco_descrp .= " - ".$enderecos->{cidade};
					}
				if($enderecos->{uf} ne "")
					{
					if($enderecos->{cidade} ne "")
						{
						$endereco_descrp .= "/";
						}
					$endereco_descrp .= $enderecos->{uf};
					}
				$endereco_descrp .= "</div>";
				}
			}
		}
	}
	
	
return true;