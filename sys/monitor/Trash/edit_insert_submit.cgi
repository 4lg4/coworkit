#!/usr/bin/perl

$nacess = "903";
require "../cfg/init.pl";

$descrp = &get('descrp');
$empresa = &get('cliente');
$endereco = &get('cliente_endereco_radios');
$host = &get('host_radios');
$hidden = &get('show_radios');

print $query->header({charset=>utf8});

if($host ne "")
	{
	$host="'".$host."'";
	}
else
	{
	$host="NULL";
	}
	
# inicia bloco SQL onde irá voltar no caso de rollback
$dbh->begin_work;
# Insere o registro
$DB = &DBE("insert into monitor_grupo (endereco, descrp, hidden, host) values ('$endereco', '$descrp', '$hidden', $host)");
if($DB > 0)
	{
	$monitor_codigo = $DB;
	
	$DB = &DBE("select * from monitor_grupo where codigo='$monitor_codigo' ");
	while($m=$DB->fetchrow_hashref)
		{
		$chave = $m->{chave};
		}
	}
else
	{
	print "<script> alerta('Falha ao incluir o monitoramento no banco de dados!');</script>";
	}

print "	<script>
		unLoadingObj('detalhe_proced');
		DMessages('Monitoramento cadastrado com sucesso!');";
if($chave ne "")
	{
	print "		alerta('<br><br>Seu código é $monitor_codigo e sua chave é $chave &nbsp;&nbsp;&nbsp;');";
	}
print "		procede.insert();
	</script>";

	
# finaliza sequência de bloco SQL com sucesso
$dbh->commit;