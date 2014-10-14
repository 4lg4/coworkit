#!/usr/bin/perl

use HTML::Entities;

$nacess = '66';
require "../cfg/init.pl";

$ID = &get('ID');
$COLETOR = &get('COLETOR');

$ACAO = &get('ACAO');

# variavel de controle se mostra data especifica
$SHOWDAY = &get('SHOWDAY');

$cliente = &get('cliente');
$solicitante = &get('solicitante');

$forma = &get('forma');
$servidor = &get('servidor');
if($servidor eq "1")
	{ $servidor = TRUE; }
else
	{ $servidor = FALSE; }
	
# $data_exec = &get('data_exec');
$data_exec = &dateToSave(&get('data_exec'));
$tempo_exec = &get('tempo_exec');
$tempo_faturado = &get('tempo_faturado');

$descrp = &get('descrp');

print $query->header({charset=>utf8});
print<<HTML;
<style>
.navigateable td
      {
      padding-left: 4px;
      }
.navigateable div
      {
      width: 99%;
      height: 1em;
      padding: 0px;
      padding-top: 1px;
      overflow: hidden;
      }
</style>

HTML


$nacess_rel = 0;
# Verifica se tem acesso aos relatórios do timesheet, para mostrar a quantidade de horas de cada usuário
$sth = $dbh->prepare("select * from usuario_menu where usuario_menu.usuario = '$LOGUSUARIO' and usuario_menu.menu = '903' ");
$sth->execute;
if($rv = $sth->rows > 0)
	{
	$nacess_rel = 1;
	}



# DEBUG
# print " <hr> $COLETOR = &get('COLETOR'); <hr> $ACAO = &get('ACAO'); <hr> $SHOWDAY = &get('SHOWDAY'); <hr> $COLETOR = &get('COLETOR'); <br><Br> $cliente = &get('cliente'); <br> $solicitante = &get('solicitante'); <br> <br>  $forma = &get('forma'); <br> $servidor = &get('servidor'); <br> <br>  $data_exec = &get('data_exec'); <br> $tempo_exec = &get('tempo_exec'); <br> $tempo_faturado = &get('tempo_faturado'); <br> <br> $descrp = &get('descrp'); <br> - $USER->{usuario} - $LOGUSUARIO ".(&timestamp("timestamp"))."  <hr>  ";
# exit;

# [INI] COLETOR DELETE -----------------------------------------------------------------------------------------------------
if($COLETOR ne "" && $ACAO eq "delete")
	{
	# sql exec
	$DB = $dbh->do("delete from coletor where codigo = $COLETOR");
	
	# se erro
	if($dbh->err ne "") {  &erroDBH($msg{db_delete}." Coletor !!!");  $dbh->rollback;  &erroDBR;  exit; } 
	
	# logger
	logger("coletor","delete","delete from coletor where codigo = $COLETOR");
	
	# retorno do script de insercao	
	print "
		<script>
			resetform();
			top.alerta('Coletor Excluido com Sucesso');
		</script>";
	
	# exit;
	}
# [END] COLETOR DELETE -----------------------------------------------------------------------------------------------------

# [INI] COLETOR NOVO -----------------------------------------------------------------------------------------------------
if($COLETOR eq "" && $ACAO eq "salvar")
	{
	# ajusta data do lancamento interna
	$dt_hj = &timestamp("timestamp");

	# sql exec
	$DB = $dbh->do("insert into coletor (data, data_exec, tempo_exec, tempo_faturado, forma, profissional, cliente, solicitante, descrp, parceiro, servidor) values ('".(&timestamp("timestamp"))."','$data_exec','$tempo_exec','$tempo_faturado','$forma','".$USER->{usuario}."',$cliente,'$solicitante','$descrp','$LOGEMPRESA', $servidor) ");
	
	# se erro
	if($dbh->err ne "") {  &erroDBH($msg{db_insert}." Coletor !!!");  $dbh->rollback;  &erroDBR;  exit; } 
	
	# logger
	logger("coletor","insert","insert into coletor (data, data_exec, tempo_exec, tempo_faturado, forma, profissional, cliente, solicitante, descrp, parceiro, servidor) values ('".(&timestamp("timestamp"))."','$data_exec','$tempo_exec','$tempo_faturado','$forma','".$USER->{usuario}."',$cliente,'$solicitante','$descrp','$LOGEMPRESA' ,$servidor)");
	
	# retorno do script de insercao	
	print "<script>resetform();</script>";
	
	# exit;
	}
# [END] COLETOR NOVO -----------------------------------------------------------------------------------------------------

# [INI] COLETOR UPDATE ---------------------------------------------------------------------------------------------------
if($COLETOR ne "" && $ACAO eq "salvar")
	{
	# sql exec
	$DB = $dbh->do("update coletor set cliente=$cliente, data_exec='$data_exec', tempo_exec='$tempo_exec', tempo_faturado='$tempo_faturado', forma='$forma', solicitante='$solicitante', descrp='$descrp', parceiro='$LOGEMPRESA', servidor=$servidor where codigo = $COLETOR");
	
	# se erro
	if($dbh->err ne "") {  &erroDBH($msg{db_update}." Coletor !!!");  $dbh->rollback;  &erroDBR;  exit; } #  se erro
	
	# logger
	logger("coletor","update","update coletor set cliente=$cliente, data_exec='$data_exec', tempo_exec='$tempo_exec', tempo_faturado='$tempo_faturado', forma='$forma', solicitante='$solicitante', descrp='$descrp', parceiro='$LOGEMPRESA', servidor=$servidor where codigo = $COLETOR");
	
	# exit;
	}
# [END] COLETOR UPDATE ---------------------------------------------------------------------------------------------------

# janela de aviso de salvamento
if($ACAO eq "salvar")
	{
	print "<script>top.alerta('Dados Salvos com Sucesso');</script>";
	}


# [INI] COLETOR SHOW -----------------------------------------------------------------------------------------------------
if($ACAO eq "show")
	{
	# sql exec
	$DB = $dbh->prepare("select coletor.*, usuario.nome as profissional_nome, coletor_forma.descrp as forma_descrp, empresa.nome as cliente_nome from coletor left join usuario on (usuario.usuario = coletor.profissional) left join coletor_forma on (coletor_forma.codigo = coletor.forma) left join empresa on (empresa.codigo = coletor.cliente) where coletor.codigo = $COLETOR  and coletor.parceiro = '$LOGEMPRESA'"); 
	$DB->execute;
	
	# se erro
	if($dbh->err ne "") {  &erroDBH($msg{db_select}." Coletor !!!");  $dbh->rollback;  &erroDBR; exit; } 
	
	# popula variavel
	$coletor = $DB->fetchrow_hashref;
	
	# teste checkbox hora servidor
	if($coletor->{servidor} == 0)
		{ $coletor->{servidor} = false; }
	else
		{ $coletor->{servidor} = true; }
	
	# ajuste da quebra de linha
	$coletor->{descrp} = &get($coletor->{descrp}, "NEWLINE_SHOW");
	
	# retorno do script de insercao	
	print "<script>
		\$('#cliente').val('$coletor->{cliente}');
		\$('#cliente_descrp').val('$coletor->{cliente_nome}');
		\$('#solicitante').val('$coletor->{solicitante}');
		\$('#forma').val('$coletor->{forma}');
		\$('#servidor').attr('checked', $coletor->{servidor});
		\$('#data_exec').val('".(&dateToShow($coletor->{data_exec}))."');
		\$('#tempo_exec').val('$coletor->{tempo_exec}');
		\$('#tempo_faturado').val('$coletor->{tempo_faturado}');
		\$('#descrp').val('".decode_entities($coletor->{descrp})."');
		\$('#profissional').text('$coletor->{profissional_nome}');
		</script>";

	exit;
	}
# [END] COLETOR SHOW -----------------------------------------------------------------------------------------------------

# exit;
	
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

# ajusta sql para mostrar dia selecionado e mes do dia em questao
if($SHOWDAY ne "")
	{
	$DATAY = substr($SHOWDAY, 0, 4);
	$DATAM = substr($SHOWDAY, 4, 2);
	$DATAD = substr($SHOWDAY, 6, 2);
	$DATA_week = "timestamp '".$DATAY."-".$DATAM."-".$DATAD." 00:00:00' ";
	}

$DATA_month = $DATAY."-".$DATAM;	
$DATA_day = $DATAY."-".$DATAM."-".$DATAD;

# ajusta visualizacao de coletores pelo nivel do usuario
# if($USER->{nivel} != 1) # se nao for adm
#	{
#	$VIEW = "and(coletor.responsavel = '$USER->{usuario}' or coletor.usuario = '$USER->{usuario}')";
#	}
	
	$SQL_BASE = " select coletor.*, usuario.nome as profissional_nome, coletor_forma.descrp as forma_descrp, empresa.nome as cliente_nome "; 
	$JOIN_BASE = " left join usuario on (usuario.usuario = coletor.profissional) left join coletor_forma on (coletor_forma.codigo = coletor.forma) left join empresa on (empresa.codigo = coletor.cliente) ";
	
	$SQL = $SQL_BASE." from coletor ".$JOIN_BASE." where parceiro = '$LOGEMPRESA' order by coletor.data_exec asc";
	$SQL_month = $SQL_BASE." from coletor ".$JOIN_BASE." where to_char(data_exec, 'YYYY-MM') = '".$DATA_month."' $VIEW and coletor.parceiro = '$LOGEMPRESA' order by coletor.data_exec desc";
	$SQL_week = $SQL_BASE.", extract(dow from data_exec) as dow_ from coletor ".$JOIN_BASE." where to_char(data_exec, 'YYYY') = '".$DATAY."' and extract(week from data_exec + interval '1 days') = extract(week from ".$DATA_week." + interval '1 days') $VIEW and coletor.parceiro = '$LOGEMPRESA' order by coletor.data_exec asc";
	$SQL_day = $SQL_BASE." from coletor ".$JOIN_BASE." where to_char(data_exec, 'YYYY-MM-DD') = '".$DATA_day."' $VIEW and coletor.parceiro = '$LOGEMPRESA' order by coletor.data_exec desc";
	$SQL_user = $SQL_BASE." from coletor ".$JOIN_BASE." where usuario.usuario like '".$USER->{usuario}."' and to_char(data_exec, 'YYYY-MM') = '".$DATA_month."' $VIEW and coletor.parceiro = '$LOGEMPRESA' order by coletor.data_exec desc";
	

#print "<hr>$SQL_month";
# debug
# print "<hr>".$SQL."<hr>".$SQL_month."<hr>".$SQL_week."<hr>".$SQL_day."<hr>";
# exit;

# header da tabela
$THEAD  = "	<thead>";
$THEAD .= "	<tr><th style='padding:2px; width:5%;'>Data</th>";
$THEAD .= "		<th style='padding:2px; width:5%;'>Duração</th>";
$THEAD .= "		<th style='padding:2px; width:10%;'>Profissional</th>";
$THEAD .= "		<th style='padding:2px; width:10%;'>Forma</th>";
$THEAD .= "		<th style='padding:2px; width:20%;'>Cliente</th>";
$THEAD .= "		<th style='padding:2px; width:8%;'>Solicitante</th>";
$THEAD .= "		<th style='padding:2px; width:40%;'>Descrição</th>";
$THEAD .= "		<th style='padding:2px; width:3%;'>Servidor</th>";
$THEAD .= "	</tr>";
$THEAD .= "	</thead>";


$coletor_id = 0;
# lista coletores do dia / Mes ------------------------------------------------------------------------------
sub SQLCOLETOR
	{ ($SQL) = shift;
	
	# zera variavel de retorno
	my $R;
	my $R_;

	# sql exec
	$DB = $dbh->prepare($SQL);
	$DB->execute;
	if($dbh->err ne "") { &erroDBH($msg{db_select}." Lista de Coletores !!!"); &erroDBR; }		
	
	while($coletor = $DB->fetchrow_hashref)
		{				
		# Data Ajusta
		if($LOGEMPRESA eq "1")
			{
			$data_exec_show = &dateToShow($coletor->{data_exec},"DATE"); # ajusta time stamp		
			}
		else
			{
			$data_exec_show = &dateToShow($coletor->{data_exec}); # ajusta time stamp		
			}
		
		# Hora servidor 
		if($coletor->{servidor} == 0)
			{ $coletor->{servidor} = "Não"; }
		else
			{ $coletor->{servidor} = "<b>Sim</b>"; }
		
		# Descrp lenght
		$coletor->{descrp} = &get($coletor->{descrp}, "NEWLINE_SHOW");
		
		$R_ .= "<tr id='day_$coletor->{codigo}' onClick=\\\"coletorEdit($coletor->{codigo});\\\"  style='cursor:pointer; height:23px;'><td style='text-align:center;'>$data_exec_show </td><td style='text-align:center;'>$coletor->{tempo_exec}</td><td><div>$coletor->{profissional_nome}</div></td><td><div>$coletor->{forma_descrp}</div></td><td><div>$coletor->{cliente_nome}</div></td><td><div>$coletor->{solicitante}</div></td><td><div>$coletor->{descrp} </div></td><td style='padding-left:4px; text-align:center;'>$coletor->{servidor} </td></tr>";
		}
		
	# monta visualizacao	
	$R  = "<table id='coletor_tb_".$coletor_id."' cellspacing='1' cellpadding='1' style='width:100%;'>";
	$R .= $THEAD;
	$R .= "	<tbody style='width:100%; '>";
	$R .= "	".$R_."";
	$R .= "	</tbody>";
	$R .= "</table>";

	$coletor_id++;	
	return $R;
	}

$R_month = &SQLCOLETOR($SQL_month);
$R_day = &SQLCOLETOR($SQL_day);
$R_user = &SQLCOLETOR($SQL_user);

# [INI] soma total de horas do mes --------------------------------------------------------------------------------------
$DB = $dbh->prepare("select sum(tempo_exec) as tempo_total from coletor where to_char(data_exec, 'YYYY-MM') = '".$DATA_month."' and profissional like '".$USER->{usuario}."' and coletor.parceiro = '$LOGEMPRESA' ");
$DB->execute;
if($dbh->err ne "") { &erroDBH($msg{db_select}." Total de Horas de Coletores !!!"); &erroDBR; }
$CT = $DB->fetchrow_hashref;
# [END] soma total de horas do mes --------------------------------------------------------------------------------------


# [INI] soma total de horas do mes dos usuarios--------------------------------------------------------------------------------------
# $DB = $dbh->prepare("select sum(tempo_exec) as tempo_total from coletor where to_char(data_exec, 'YYYY-MM') = '".$DATA_month."' and profissional like '".$USER->{usuario}."'");
$DB = $dbh->prepare("select sum(tempo_exec) as tempo_total, sum(tempo_faturado) as tempo_faturado from coletor where to_char(data_exec, 'YYYY-MM') = '".$DATA_month."' and coletor.parceiro = '$LOGEMPRESA'");
$DB->execute;
if($dbh->err ne "") { &erroDBH($msg{db_select}." Total de Horas de Coletores !!!"); &erroDBR; }
$CT2 = $DB->fetchrow_hashref;


# $SQL_month = $SQL_BASE." from coletor ".$JOIN_BASE." where to_char(data_exec, 'YYYY-MM') = '".$DATA_month."' $VIEW order by coletor.data_exec desc";
# $USER->{usuario}



# [INI] lista de horas de clientes ---------------------------------------------------------------------------------------------------
$DATA_month = $DATAY."-".$DATAM;
$DB = $dbh->prepare("select cliente, sum(tempo_exec) as tempo_total, sum(tempo_faturado) as tempo_faturado from coletor where to_char(data_exec, 'YYYY-MM') = '".$DATA_month."' and coletor.parceiro = '$LOGEMPRESA' group by cliente order by tempo_total desc");
$DB->execute;
if($dbh->err ne "") {  &erroDBH($msg{db_select}." lista de horas por cliente !!!");  &erroDBR;  exit;  } # se erro
while($hora_empresa = $DB->fetchrow_hashref)
	{
	$DB_emp = $dbh->prepare("select nome from empresa where codigo = $hora_empresa->{cliente}");
	$DB_emp->execute;
	$cliente = $DB_emp->fetchrow_hashref;
	
	$hours_emp .= "<tr id='emp_".$hora_empresa->{cliente}."' onClick=\\\"glow('emp_".$hora_empresa->{cliente}."')\\\"><td>".$cliente->{nome}."</td><td align=right>".$hora_empresa->{tempo_total}."</td><td align=right>".$hora_empresa->{tempo_faturado}."</td></tr>";
	}
$relatorio_empresa = "<table id='coletor_empresas_tb' width=100%><thead><tr><th>Nome</th><th width=15%>Total Horas</th><th width=15%>Total Faturado</th></tr></thead><tbody>";
$relatorio_empresa .= $hours_emp;
$relatorio_empresa .= "</tbody>";
if($CT2->{tempo_total} ne "")
	{
	$relatorio_empresa .= "<tfoot><tr><td class=navigateable_th style='text-align: right'>Data $DATAM/$DATAY - Total Horas</td><td class=navigateable_th align=right>$CT2->{tempo_total}</td><td class=navigateable_th align=right>$CT2->{tempo_faturado}</td></tfoot></tr>";
	}
$relatorio_empresa .= "</table>";
# [END] lista de horas de clientes ---------------------------------------------------------------------------------------------------



if($nacess_rel == 1)
	{
	# gera lista separada por usuario
	$sth = $dbh->prepare("select * from usuario where bloqueado is null and usuario.empresa = '$LOGEMPRESA' and usuario.usuario not like 'admin' order by nome asc");
	$sth->execute;
	if($dbh->err ne "") {  &erroDBH($msg{db_select}." lista de usuarios !!!");  &erroDBR;  exit;  } # se erro
	$usr_cod=0;
	while($usuario = $sth->fetchrow_hashref)
		{
		$DB = $dbh->prepare("select sum(tempo_exec) as tempo_total, sum(tempo_faturado) as tempo_faturado from coletor where to_char(data_exec, 'YYYY-MM') = '".$DATA_month."' and profissional like '".$usuario->{usuario}."' ");
		$DB->execute;
		if($dbh->err ne "") { &erroDBH($msg{db_select}." Total de Horas de Coletores !!!"); &erroDBR; }
		$hora2 = $DB->fetchrow_hashref;
		if($hora2->{tempo_total} eq "")
			{
			$hora2->{tempo_total} = "00:00:00";
			}
		if($hora2->{tempo_faturado} eq "")
			{
			$hora2->{tempo_faturado} = "00:00:00";
			}
		$hours .= "<tr id='usr_".$usr_cod."' onClick=\\\"glow('usr_".$usr_cod."')\\\"><td>".$usuario->{nome}."</td><td width=15% align=right>".$hora2->{tempo_total}."</td><td width=15% align=right>".$hora2->{tempo_faturado}."</td></tr>";
		$usr_cod++;
		}
	$relatorio_usuario = "<table id='relatorio_usuarios_tb' width=60%><thead><tr><th>Nome</th><th width=15%>Total Horas</th><th width=15%>Horas Faturadas</th></tr></thead><tbody>";
	$relatorio_usuario .= $hours;
	$relatorio_usuario .= "</tbody>";
	$relatorio_usuario .= "<tfoot><tr><td class=navigateable_th style='text-align: right'>Data $DATAM/$DATAY - Total Horas</td><td class=navigateable_th align=right>$CT2->{tempo_total}</td><td class=navigateable_th align=right>$CT2->{tempo_faturado}</td></tfoot></tfoot></tr>";
	$relatorio_usuario .= "</table>";
	# [END] soma total de horas do mes dos usuarios --------------------------------------------------------------------------------------
	}






print "	
	<script>
		\$(\"#coletor_day\").html(\"$R_day\");
		new grid('coletor_tb_1');

		\$(\"#coletor_month\").html(\"$R_month\");
		new grid('coletor_tb_0');

		\$(\"#total_mes\").text(\"$CT->{tempo_total}\");
		\$(\"#coletor_user\").html(\"$R_user\");
		new grid('coletor_tb_2');

		\$(\"#total_cliente\").text(\"$CT2->{tempo_total}\");
		\$(\"#coletor_empresa\").html(\"$relatorio_empresa\");
		coletor_empresas = new grid('coletor_empresas_tb');
	";
if($nacess_rel == 1)
	{
	print "

		\$(\"#relatorio_usuario\").html(\"$relatorio_usuario\");
		relatorio_usuarios = new grid('relatorio_usuarios_tb');

	";
	}
print "
	</script>
	";

exit;
