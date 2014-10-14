#!/usr/bin/perl

$nacess = '66';
require "../../cfg/init.pl";

$ID = &get('ID');
$RELATORIO = &get('RELATORIO');

$empresa_class = &get('empresa_class');
if($empresa_class eq "2")
	{
	$cliente = NULL;
	$tipo = "misto";
	}
else
	{
	$cliente = &get('cliente');
	$tipo = &get('tipo');
	}

$obs = &get('obs');
$data_ini = &get('data_ini');
$data_fim = &get('data_fim');
@faturado = &get_array('faturado');

# corrige datas para pesquisa --
if($data_ini ne "")
	{
	$DATAY = substr($data_ini, 6, 4);
	$DATAM = substr($data_ini, 3, 2);
	$DATAD = substr($data_ini, 0, 2);
	$DATA_ini = $DATAY."-".$DATAM."-".$DATAD;
	$DATA_ini_c = $DATAY."".$DATAM."".$DATAD;
	}
if($data_fim ne "")
	{
	$DATAY = substr($data_fim, 6, 4);
	$DATAM = substr($data_fim, 3, 2);
	$DATAD = substr($data_fim, 0, 2);
	$DATA_fim = $DATAY."-".$DATAM."-".$DATAD;
	$DATA_fim_c = $DATAY."".$DATAM."".$DATAD;
	}
if($DATA_ini_c > $DATA_fim_c)
	{
	$DATA_ini2 = $DATA_fim;
	$DATA_fim = $DATA_ini;
	$DATA_ini = $DATA_ini2;
	}

# controla data para mostrar
if($DATA ne "" && $DATA ne "undefined")
	{
	$DATAY = substr($DATA, 0, 4);
	$DATAM = substr($DATA, 4, 2);
	$DATAD = substr($DATA, 6, 2);
	$DATA_week = "timestamp '".$DATAY."-".$DATAM."-".$DATAD." 00:00:00' ";
	}
else
	{
	$DATAY = timestamp("year");
	$DATAM = timestamp("month");
	$DATAD = timestamp("day");
	$DATA_week = "now()";
	}

$DATA_month = $DATAY."-".$DATAM;
$DATA_day = $DATAY."-".$DATAM."-".$DATAD;
$entre_datas = " (to_char(data_exec, 'YYYY-MM-DD') >= '".$DATA_ini."' and to_char(data_exec, 'YYYY-MM-DD') <= '".$DATA_fim."') ";

print $query->header({charset=>utf8});

# debug("$SHOWDAY - $SHOWMONTH");
# DEBUG
# debug($entre_datas);
# debug("<hr>classif. empresa $empresa_class <br> Servidor: $servidor <br> Servidor Misto $servidor_misto <br><br>$entre_datas <hr> $ID = &get('ID'); <br> $RELATORIO = &get('RELATORIO'); <br> $ACAO = &get('ACAO'); <br> $cliente = &get('cliente'); <br> $obs = &get('obs'); <br> $servidor = &get('servidor'); <br> $servidor_misto = &get('servidor_misto'); <br> $data_ini = &dateToSave(&get('data_ini')); <br> $data_fim = &dateToSave(&get('data_fim'));  <br>  $empresa_class = &get('empresa_class') <hr>");
# exit;

# [INI] Relatorio NOVO -----------------------------------------------------------------------------------------------------

# ajuste para relatorio de servidor
if($tipo eq "servidor")
	{
	$rserver = " and tipo = 'servidor' ";
	$hserver = " and servidor is true ";
	}
elsif($tipo eq "noservidor")
	{
	$rserver = " and tipo = 'noservidor' ";
	$hserver = " and servidor is false ";
	}
else
	{
	$rserver = " and tipo = 'misto' ";
	$hserver = " ";
	}

if($empresa_class eq "2")
	{
	# Avulso
	$sql_empresa_class = "and (empresa_relacionamento.relacionamento != 6 or empresa_relacionamento.relacionamento is null) ";
	$cliente = NULL;
	}
else
	{
	# Cliente Mensalistas
	$sql_empresa_class = "and empresa_relacionamento.relacionamento = 6 ";
	$sql_cliente = "and coletor.cliente = $cliente";
	}

if(@faturado < 2)
	{
	if($faturado[0] eq "sim")
		{
		$sql_faturado = "and tempo_faturado != '00:00:00'";
		}
	elsif($faturado[0] eq "nao")
  		{
		$sql_faturado = "and tempo_faturado = '00:00:00'";
		}
	}



# SYSCALL, sql antigo -> $DBC = $dbh->prepare("select coletor.*, usuario.nome as profissional_nome, coletor_forma.descrp as forma_descrp, empresa.nome as cliente_nome, empresa.codigo as cliente_codigo from coletor left join usuario on (usuario.usuario = coletor.profissional) left join coletor_forma on (coletor_forma.codigo = coletor.forma) left join empresa on (empresa.codigo = coletor.cliente) left join empresa_relacionamento on empresa.codigo = empresa_relacionamento.empresa where $entre_datas $sql_cliente $hserver $sql_empresa_class $sql_faturado and coletor.parceiro = '$LOGEMPRESA' order by coletor.data_exec desc");
$DBC = $dbh->prepare("select c.*, u.nome as tecnico_nome, e.nome as cliente_nome, e.codigo as cliente_codigo from chamado as c left join usuario as u on (u.usuario = c.tecnico) left join empresa_endereco as ee on (ee.codigo = c.cliente_endereco) left join empresa as e on (e.codigo = ee.empresa) where (to_char(c.data_agendamento, 'YYYY-MM-DD') >= '2013-03-01' and to_char(c.data_agendamento, 'YYYY-MM-DD') <= '2013-03-13') order by c.data_agendamento desc");
$DBC->execute;

if($dbh->err ne "") { &erroDBH($msg{db_select}." Lista de Coletores !!!"); &erroDBR; }
if($DBC->rows == 0)
	{
	print "<script>top.alerta('Nenhum lançamento encontrado para essa pesquisa'); </script>";
	exit;
	}
	
# EOS amostra funcionamento
else
	{
	# gera lista
	print "<table border=1>";
	print "<tr><td>Data Agendamento / Execução</td><td>Tempo Gasto</td><td>Cliente Nome</td><td>Solicitante</td><td>Descrição</td><td>Tecnico</td></tr>";
	while($coletor = $DBC->fetchrow_hashref)
		{
		# Data Ajusta
		$coletor->{data_agendamento} = &dateToShow($coletor->{data_agendamento}); # ajusta time stamp
		$coletor->{tempo_agendamento} = &dateToShow($coletor->{tempo_agendamento}); # ajusta time stamp

		print "<tr><td>$coletor->{data_agendamento}</td><td>$coletor->{tempo_agendamento}</td><td>$coletor->{cliente_nome}</td><td>$coletor->{usuario}</td><td>$coletor->{descrp}</td><td>$coletor->{tecnico_nome}</td></tr>";
		}
	print "</table>";
	}

exit;


# insere dados do relatorio pai sql exec
$DB = $dbh->do("insert into coletor_relatorio (data, data_ini, data_fim, cliente, obs, tipo, usuario, parceiro) values ('".(&timestamp("timestamp"))."','$data_ini','$data_fim',$cliente,'$obs','$tipo','".$USER->{usuario}."', '$LOGEMPRESA') ");

# se erro
if($dbh->err ne "") {  &erroDBH($msg{db_insert}." Relatorio Pai !!!");  $dbh->rollback;  &erroDBR;  exit; }

# recupera codigo inserido
$DB = $dbh->prepare("select currval('coletor_relatorio_codigo_seq')");
$DB->execute;

# se erro
if($dbh->err ne "") {  &erroDBH($msg{db_select}." código Relatorio Pai !!!");  $dbh->rollback;  &erroDBR; exit; } #  se erro

# ajusta variaveis
$rel = $DB->fetch;
$RELATORIO = @$rel[0];

# gera lista
while($coletor = $DBC->fetchrow_hashref)
	{
	# Data Ajusta
	$data_exec_show = &dateToShow($coletor->{data_exec},"DATE"); # ajusta time stamp

	$DADOS .= " ($RELATORIO,'$coletor->{data_exec}','$coletor->{tempo_exec}','$coletor->{tempo_faturado}','$coletor->{forma_descrp}','$coletor->{profissional_nome}','$coletor->{solicitante}','$coletor->{descrp}','$coletor->{servidor}',$coletor->{cliente_codigo}), ";
	}

$DADOS = substr($DADOS, 0,-2); # remove ultima virgula

# insere dados do ralatorio data
$DB = $dbh->do("insert into coletor_relatorio_data (pai, data_exec, tempo_exec, tempo_faturado, forma, profissional, solicitante, descrp, servidor, cliente) values $DADOS ;");
# se erro
if($dbh->err ne "") {  &erroDBH($msg{db_insert}." Relatorios Data !!!");  $dbh->rollback;  &erroDBR;  exit; }

# retorno do script de insercao
# print "<script>resetform();</script>";

# [END] Relatorio NOVO -----------------------------------------------------------------------------------------------------

# [INI] COLETOR SHOW -----------------------------------------------------------------------------------------------------
if($RELATORIO ne "")
	{
	print "

	<br><br><div class='rounded' style='background:#e5e5e5; padding: 20px 50px 0px 50px;'>
		<span class=title style='color:#666; font-size:10px;'><h2>Foi gerado um novo relatório baseado nos parâmetros informados.<br>Automaticamente será aberto um pop-up com o relatório para impressão em PDF.<br></span>
		<span class=title style='color:#666; font-size:10px;'><h2>Caso você possua bloqueio de pop-up, libere o acesso em seu navegador. Você também pode <a href='javascript:imprimir()' tarbet='_blank' style='text-decoration: underline'>clicar aqui</a> abrir a impressão.<br></span>
		<span class=title style='color:#666; font-size:10px;'><h2>Você também pode exportar esse relatório para o excel, <a href='javascript:exportar()' tarbet='_blank' style='text-decoration: underline'>clicando aqui</a>.</span>
	</div>

	<script language='JavaScript'>
	\$('#RELATORIO').val($RELATORIO);
	imprimir();
	</script>
	";

	}
# [END] COLETOR SHOW -----------------------------------------------------------------------------------------------------

exit;
