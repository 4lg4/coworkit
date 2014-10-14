#!/usr/bin/perl

$nacess = "999";
require "../../cfg/init.pl"; #ou ../cfg/init.pl
$ID = &get('ID');
$COD = &get('COD');
$MODO = &get('MODO');

$empresa = &get('empresa');
$proced = &get('proced');
$externo = &get('externo');
$endereco = &get('endereco');

print $query->header({charset=>utf8});

#Se for acesso direto do grid
if($externo ne "")
	{
	#Puxa todas as empresas 
	$DB1 = &DBE("select * from empresa where codigo='$externo' order by nome ");

	#Puxa todas as empresa e monta o grid
	while($empresas = $DB1->fetchrow_hashref)
		{
		#variavel que recebe os dados para montagem do DTOUCHRADIO - array
		$empresas_list .= "{val:'$empresas->{codigo}',descrp:'<left>$empresas->{nome}</left>'},";
		}
	
	$empresas_list = substr($empresas_list, 0,-1); # remove ultima virgula
	
	#Popula
	print "<script> 
			//Monta a lista
			\$('#empresas_list').DTouchRadio(
				{
				addItem:[$empresas_list], 
				orientation:'vertical',
				//Evento ao clicar
				DTouchRadioClick: function()
						{
						//Pega o código do item clicado.
						enderecos(\$('#empresas_list').DTouchRadio('DTouchRadioGetValue'));	
						},
				uncheck: false
				});
			
			\$('#empresas_list').DTouchRadio('DTouchRadioSetValue',$externo);
			\$('#CAD input[name=empresa_aux]').val('$externo');
			\$('#externo').val('');
			procede('$externo');
		</script>";
	}
#Se for parceiro done ou done
if($empresa eq "" && $endereco eq "" && $proced eq "")
	{
	#Puxa todas as empresas 
	$DB1 = &DBE("select * from empresa join parceiro_empresa on empresa.codigo = parceiro_empresa.empresa and parceiro_empresa.parceiro = '$LOGEMPRESA'");
	
	#Popula por primeira a linha proced. sem tarefa
	
	$empresas_list="{val:'null',descrp:'Procedimentos sem empresa'},";

	#Puxa todas as empresa e monta o grid
	while($empresas = $DB1->fetchrow_hashref)
		{
		#variavel que recebe os dados para montagem do DTOUCHRADIO - array
		$empresas_list .= "{val:'$empresas->{codigo}',descrp:'<left>$empresas->{nome}</left>'},";
		}
	
	$empresas_list = substr($empresas_list, 0,-1); # remove ultima virgula
	
	#Popula
	print "<script> 
			unLoadingObj('bloco_empresas');
			//Monta a lista
			\$('#empresas_list').DTouchRadio(
				{
				addItem:[$empresas_list], 
				orientation:'vertical',
				//Evento ao clicar
				DTouchRadioClick: function()
						{
						//Pega o código do item clicado.
						enderecos(\$('#empresas_list').DTouchRadio('DTouchRadioGetValue'));	
						},
				uncheck: false
				});			
		</script>";
	}
#Exibe lista de enderecos
if($empresa ne "" && $endereco eq "" && $proced eq "")
	{
	
	if($empresa ne "null")
		{
		#Pega os endereços da empresa
		$DB2 = &DBE("select * from empresa_endereco where empresa = '$empresa' order by codigo");
		
		#Verifica se existem
		if($DB2->rows()>0)
			{
			#Se existir ele puxa todos
			while($enderecos = $DB2->fetchrow_hashref)
				{
				#Insero no formulario de inclusão os endereços da empresa
				$endereco_descrp .="<div id='endereco_$enderecos->{codigo}' style='display:none'> <input type='radio' id='endereco' name='endereco' value='$enderecos->{codigo}'> $enderecos->{endereco} </div>";
				
				$endereco_list .="{val:'$enderecos->{codigo}',descrp:'$enderecos->{endereco}'},";
				}
			}
			
		#Popula	
		print "<script>
			//Insere os radios dos endereços
			\$('#bloco_proced').hide();
			 \$('#bloco_endereco').fadeIn();
			 
			
			//Limpa o cache do DTouch
			\$('#endereco_list').DTouchRadio('DTouchRadioReset','hard');
			\$('#proced_list').DTouchRadio('DTouchRadioReset','hard');
			
			//Popula o DTouchRadio
			\$('#endereco_list').DTouchRadio({
				addItem:[$endereco_list],
				orientation:'vertical',
				DTouchRadioClick: function()
						{
						proced_list(\$('#endereco_list').DTouchRadio('DTouchRadioGetValue'));
						},
				DTouchRadioUncheck: function()
					{
					\$('#bloco_dones').fadeOut();
					\$('#bloco_form').fadeOut();
					}
				});
				
			\$('#empresa').val('$empresa');
			</script>";
		}
	else
		{
		#Popula	
		print "<script>
			\$('#enderecos').html(\"<input type='radio' style='display:none' id='endereco' name='endereco' value='null'>\");
			
			 \$('#bloco_endereco').hide();
			 \$('#bloco_proced').fadeIn();
			 proced_list('null');
			</script>";
		}
		
	}
	
#Exibe lista de hotst/dones/users do endereco
if($endereco ne "")
	{
	#Puxa todos os procedimentos do endereço respectivamente
	$DB3 = &DBE("select *, d.codigo AS cod_dones from dones d join ti_hosts AS hs on hs.codigo=d.ti_hosts join ti_users AS us on us.codigo=d.ti_users where d.endereco=$endereco ");
	
	
	#Se tem proced. no endereco
	if($DB3->rows()>0)
		{
		#Se tiver puxa
		while($proced = $DB3->fetchrow_hashref)
			{
			$proced_list .="{val:'$proced->{cod_dones}',descrp:'<left><b>HOSTNAME:</b> $proced->{hostname} - <b>USER:</b> $proced->{usuario}</left>'},";
			$positivo++;
			}
		}
		
	#Pega os domain para fazer regex e montar o select
	$DB_HOST = &DBE("select * from dones_domains");
	#Inicia o select
	$dones_domains = "<select name='dones_domains' id='dones_domains'>";
	
	while($RS_HOST=$DB_HOST->fetchrow_hashref)
		{
		#preenche o conteudo do select
		$dones_domains .="<option value='$RS_HOST->{codigo}'>$RS_HOST->{descrp}</option>"
		}
	#finaliza o select
	$dones_domains .="</select>";
		
	#Popula	
	print "<script>
		menu_dones.btnHideAll(); menu_dones.btnShow(['icon_insert','icon_cancel']);
		\$('#dones_list').DTouchRadio('DTouchRadioReset','hard');
		\$('#dones_list').DTouchRadio({
			addItem:[$proced_list], 
			orientation:'vertical',
			DTouchRadioClick: function()
					{
					detalhe_proced(\$('#dones_list').DTouchRadio('DTouchRadioGetValue'));	
					},
			DTouchRadioUncheck: function()
					{
					\$('#bloco_form').fadeOut();
					}
			});
			
		//Marca o endereço
		\$('#CAD input[name=endereco]').each(function()
			{
			\$(this).parent('#endereco_'+\$(this).val()).css('display','none');
			if(\$(this).val()=='$endereco')
				{
				\$(this).parent('#endereco_$endereco').css('display','block');
				\$(this).prop('checked','true');
				}
			});
		\$('#endereco').val($endereco);
		
		\$('#domain').html(\"$dones_domains\");
		\$('#dones_domains').change(function() { LimpaString(\$('#hostname')); check_host(); });
		
		</script>";
	}
	
#Exibe o procedimento  (detalhes proced)
if($proced ne "" || $proced eq "null")
	{

	$DB1 = &DBE("select * from dones d join ti_hosts AS hs on hs.codigo=d.ti_hosts join ti_users AS us on us.codigo=d.ti_users where d.codigo='$proced'");	


	while($proced = $DB1->fetchrow_hashref)
		{
		$hostname=$proced->{hostname};
		
		#Pega os domain para fazer regex e montar o select
		$DB_HOST = &DBE("select * from dones_domains");
		#Inicia o select
		$dones_domains = "<select name='dones_domains' id='dones_domains'>";
		
		while($RS_HOST=$DB_HOST->fetchrow_hashref)
			{
			#Faz a regex retirando os domain da string
			if($hostname=~ s/.$RS_HOST->{descrp}//gm)
				{
				$select_domain=$RS_HOST->{codigo};
				}
			#preenche o conteudo do select
			$dones_domains .="<option value='$RS_HOST->{codigo}'>$RS_HOST->{descrp}</option>"
			}
		#finaliza o select
		$dones_domains .="</select>";
		
		print "<script> 
			\$('#hostname').val(\"$hostname\");
			\$('#usuario').val(\"$proced->{usuario}\");
			\$('#senha').val(\"$proced->{pwd}\");
			\$('#obs_user').val(\"$proced->{descrp}\");
			
			\$('#domain').html(\"$dones_domains\");
			\$('#dones_domains').change(function() { LimpaString(\$('#hostname')); check_host(); });
			
			//Marca o endereço
			\$('#dones_domains').val('$select_domain');
			
			var host_verifica='$hostname';
			var user_verifica='$proced->{usuario}';
			var domain_verifica=\$('#dones_domains').find(':selected').text();
			</script>";
		}
	}
	
	
	