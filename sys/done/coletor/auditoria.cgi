#!/usr/bin/perl

$nacess = '66';
require "../../cfg/init.pl";

$userfilter =  &get('adt_usuario');
$data_ini = &get('adt_data_ini');
$data_fim = &get('adt_data_fim');


# corrige datas para pesquisa --
$orderby = "logger.data desc";
if($data_ini ne "")
	{
	$DATAY = substr($data_ini, 6, 4);
	$DATAM = substr($data_ini, 3, 2);
	$DATAD = substr($data_ini, 0, 2);
	$DATA_ini = $DATAY."-".$DATAM."-".$DATAD;
	$DATA_ini_c = $DATAY."".$DATAM."".$DATAD;
	#$orderby = "logger.data";
	}
if($data_fim ne "")
	{
	$DATAY = substr($data_fim, 6, 4);
	$DATAM = substr($data_fim, 3, 2);
	$DATAD = substr($data_fim, 0, 2);
	$DATA_fim = $DATAY."-".$DATAM."-".$DATAD;
	$DATA_fim_c = $DATAY."".$DATAM."".$DATAD;
	#$orderby = "logger.data desc";
	}
if($data_ini ne "" && $data_fim ne "")
	{
	if($DATA_ini_c > $DATA_fim_c)
		{ 
		$DATA_ini2 = $DATA_fim;
		$DATA_fim = $DATA_ini; 
		$DATA_ini = $DATA_ini2;
		}
	}

# monta SQL dos filtros
$sqlplus = "";
if($userfilter ne "")
      {
      $sqlplus .= " and logger.usuario = '$userfilter' ";
      }
if($DATA_ini ne "")
      {
      $sqlplus .= " and to_char(logger.data, 'YYYY-MM-DD') >= '".$DATA_ini."' ";
      }
if($DATA_fim ne "")
      {
      $sqlplus .= " and to_char(logger.data, 'YYYY-MM-DD') <= '".$DATA_fim."' ";
      }


print $query->header({charset=>utf8});

# [INI] Logger somente do Coletor  ---------------------------------------------------------------------------------------------------
$DB = $dbh->prepare("select logger.*, usuario.nome as usuario_nome from logger left join usuario on usuario.usuario like logger.usuario where logger.tabela like 'coletor' $sqlplus order by $orderby limit 1000");
$DB->execute;
if($dbh->err ne "") {  &erroDBH($msg{db_select}." lista de horas por cliente !!!");  &erroDBR;  exit;  } # se erro
$log_cod=0;
while($logger = $DB->fetchrow_hashref)
	{
	$logger_list .= "<tr id='log_".$log_cod."' onClick=\\\"glow('log_".$log_cod."')\\\"><td>".(&dateToShow($logger->{data}))."</td><td>".$logger->{usuario_nome}."</td><td>".$logger->{acao}."</td><td>".(&get($logger->{descrp},'NEWLINE'))."</td></tr>";
	$log_cod++;
	}
$R_logger = "<table id='coletor_logger_tb' width='100%'><thead><tr><th width=10%>Data</th><th width=20%>Usuário</th><th width=5%>Ação</th><th>Descrição</th></tr></thead><tbody>";
$R_logger .= $logger_list;
$R_logger .= "</tbody></table>";
# [END] Logger somente do Coletor  ---------------------------------------------------------------------------------------------------

print $R_logger;

print<<HTML;
	<script>
	\$('#coletor_logger').show();
	</script>
HTML

exit;
