#!/usr/bin/perl

$nacess = "660";
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('NF');

$ACAO = &get('ACAO');

# variavel de controle se mostra data especifica
$SHOWDAY = &get('SHOWDAY');

$cliente = &get('cliente');
$data_emissao = &dateToSave(&get('data_emissao'));
$data_vcto = &dateToSave(&get('data_vcto'));
$obs = &get('obs');
$nf_num = &get('nf_num');
$d1 = &get('d1');
$d2 = &get('d2');
$d3 = &get('d3');
$v1 = &get('v1');
$v2 = &get('v2');
$v3 = &get('v3');

print "Content-type: text/html\n\n";

# DEBUG
# print " <hr> $COD = &get('NF'); <hr> $ACAO = &get('ACAO'); <hr> $SHOWDAY = &get('SHOWDAY'); <hr> $COD = &get('NF'); <br><Br> $cliente = &get('cliente'); <br> $solicitante = &get('solicitante'); <br> <br>  $forma = &get('forma'); <br> $servidor = &get('servidor'); <br> <br>  $data_emissao = &get('data_emissao'); <br> $tempo_exec = &get('tempo_exec'); <br> $tempo_faturado = &get('tempo_faturado'); <br> <br> $descrp = &get('descrp'); <br> - $USER->{usuario} - $LOGUSUARIO ".(&timestamp("timestamp"))."  <hr>  ";
# exit;

# [INI] NF DELETE -----------------------------------------------------------------------------------------------------
if($COD ne "" && $ACAO eq "delete")
	{
	# sql exec
	$DB = $dbh->do("delete from nf where codigo = $COD");
	
	# se erro
	if($dbh->err ne "") {  &erroDBH($msg{db_delete}." N.F. !!!");  $dbh->rollback;  &erroDBR;  exit; } 
	
	# logger
	logger("nf","delete","delete from nf where codigo = $COD");
	
	# retorno do script de insercao	
	print "
		<script>
			resetform();
			// alerta('N.F. Excluido com Sucesso');
		</script>";
	
	# exit;
	}
# [END] NF DELETE -----------------------------------------------------------------------------------------------------

# [INI] NF NOVO -----------------------------------------------------------------------------------------------------
if($COD eq "" && $ACAO eq "salvar")
	{
	# ajusta data do lancamento interna
	$dt_hj = &timestamp("timestamp");

	# sql exec
	$DB = $dbh->do("insert into nf (data, data_emissao, data_vcto, nf_num, obs, cliente, usuario, d1, d2, d3, v1, v2, v3) values ('".(&timestamp("timestamp"))."','$data_emissao','$data_vcto','$nf_num','$obs',$cliente,'".$USER->{usuario}."','$d1', '$d2', '$d3', '$v1', '$v2', '$v3') ");
	
	# se erro
	if($dbh->err ne "") {  &erroDBH($msg{db_insert}." N.F. !!!");  $dbh->rollback;  &erroDBR;  exit; } 
	
	# logger
	logger("nf","insert","insert into nf (data, data_emissao, data_vcto, nf_num, obs, cliente, usuario, d1, d2, d3, v1, v2, v3) values ('".(&timestamp("timestamp"))."','$data_emissao','$data_vcto','$nf_num','$obs',$cliente,'".$USER->{usuario}."','$d1', '$d2', '$d3', '$v1', '$v2', '$v3') ");
	
	# retorno do script de insercao	
	print "<script>resetform();</script>";
	
	# exit;
	}
# [END] NF NOVO -----------------------------------------------------------------------------------------------------

# [INI] NF UPDATE ---------------------------------------------------------------------------------------------------
if($COD ne "" && $ACAO eq "salvar")
	{
	# sql exec
	$DB = $dbh->do("update nf set cliente=$cliente, data_emissao='$data_emissao', data_vcto='$data_vcto', nf_num='$nf_num', obs='$obs', d1='$d1', d2='$d2', d3='$d3', v1='$v1', v2='$v2', v3='$v3' where codigo = $COD");
	
	# se erro
	if($dbh->err ne "") {  &erroDBH($msg{db_update}." N.F. !!!");  $dbh->rollback;  &erroDBR;  exit; } #  se erro
	
	# logger
	logger("nf","update","update nf set cliente=$cliente, data_emissao='$data_emissao', data_vcto='$data_vcto', nf_num='$nf_num', obs='$obs', d1='$d1', d2='$d2', d3='$d3', v1='$v1', v2='$v2', v3='$v3' where codigo = $COD");
	
	# exit;
	}
# [END] NF UPDATE ---------------------------------------------------------------------------------------------------

# janela de aviso de salvamento
# if($ACAO eq "salvar")
#	{
#	print "<script>alerta('Dados Salvos com Sucesso');</script>";
#	}


# [INI] NF SHOW -----------------------------------------------------------------------------------------------------
if($ACAO eq "show")
	{
	# sql exec
	$DB = $dbh->prepare("select nf.*, regexp_replace(regexp_replace(nf.v1::money::text, '[R\$.]', '', 'g'),',','.')::numeric as vc1, regexp_replace(regexp_replace(nf.v2::money::text, '[R\$.]', '', 'g'),',','.')::numeric as vc2, regexp_replace(regexp_replace(nf.v3::money::text, '[R\$.]', '', 'g'),',','.')::numeric as vc3, empresa.nome as cliente_nome from nf left join empresa on (empresa.codigo = nf.cliente) where nf.codigo = $COD"); 
	$DB->execute;
	
	# se erro
	if($dbh->err ne "") {  &erroDBH($msg{db_select}." N.F. !!!");  $dbh->rollback;  &erroDBR; exit; } 
	
	# popula variavel
	$nf = $DB->fetchrow_hashref;
		
	# ajuste da quebra de linha
	$nf->{obs} = &get($nf->{obs}, "NEWLINE_SHOW");
	
	$total = $nf->{vc1} + $nf->{vc2} + $nf->{vc3};
	
	# $nf->{vc1} =~ s/\.//gm;
	
	# $nf->{vc2} =~ s/R\$//gm;
	# $nf->{vc2} =~ s/\.//gm;
	
	$nf->{v1} =~ s/R\$//gm;
	$nf->{v2} =~ s/R\$//gm;
	$nf->{v3} =~ s/R\$//gm;
	$total = money($total);
	
	$total =~ s/R\$//gm;
	# $total =~ s/\,//gm;
	# $total =~ s/\.//gm;
	

	
	# retorno do script de insercao	
	print "<script>
		\$('#nf_num').val('$nf->{nf_num}');
		\$('#cliente').val('$nf->{cliente}');
		\$('#cliente_descrp').val('$nf->{cliente_nome}');
		\$('#data_emissao').val('".(&dateToShow($nf->{data_emissao},"DATE"))."');
		\$('#data_vcto').val('".(&dateToShow($nf->{data_vcto},"DATE"))."');
		\$('#obs').val('$nf->{obs}');
		\$('#d1').val('$nf->{d1}');
		\$('#d2').val('$nf->{d2}');
		\$('#d3').val('$nf->{d3}');
		\$('#v1').val('$nf->{v1}');
		\$('#v2').val('$nf->{v2}');
		\$('#v3').val('$nf->{v3}');
		\$('#nf_total').val('$total');
		</script>";

	exit;
	}
# [END] NF SHOW -----------------------------------------------------------------------------------------------------

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

	$SQL_BASE = " select nf.*, regexp_replace(regexp_replace(nf.v1::money::text, '[R\$.]', '', 'g'),',','.')::numeric as vc1, regexp_replace(regexp_replace(nf.v2::money::text, '[R\$.]', '', 'g'),',','.')::numeric as vc2, regexp_replace(regexp_replace(nf.v3::money::text, '[R\$.]', '', 'g'),',','.')::numeric as vc3, empresa.nome as cliente_nome "; 
	$JOIN_BASE = " left join empresa on (empresa.codigo = nf.cliente) ";
	
	$SQL = $SQL_BASE." from nf ".$JOIN_BASE." order by nf.data_emissao asc";
	$SQL_month = $SQL_BASE." from nf ".$JOIN_BASE." where to_char(data_emissao, 'YYYY-MM') = '".$DATA_month."' $VIEW order by nf_num asc, nf.data_emissao desc";
	$SQL_day = $SQL_BASE." from nf ".$JOIN_BASE." where to_char(data_emissao, 'YYYY-MM-DD') = '".$DATA_day."' $VIEW order by nf_num asc, nf.data_emissao desc";
	$SQL_all = $SQL_BASE." from nf ".$JOIN_BASE." order by nf.nf_num desc";


# header da tabela
$THEAD  = "	<thead>";
$THEAD .= "	<tr>";
$THEAD .= "		<th style='display:none; width:5%;'>cod</th>";
$THEAD .= "	 	<th style='padding:2px; width:20%;'>Cliente</th>";
$THEAD .= "		<th style='padding:2px; width:5%;'>N.F.</th>";
$THEAD .= "		<th style='padding:2px; width:5%;'>Data Emissão</th>";
$THEAD .= "		<th style='padding:2px; width:5%;'>Data Vencimento</th>";
$THEAD .= "		<th style='padding:2px; width:8%;'>Valor Total</th>";
$THEAD .= "	</tr>";
$THEAD .= "	</thead>";


# lista nfes do dia / Mes ------------------------------------------------------------------------------
sub SQLNF
	{ ($SQL,$tb) = @_;
	
	# zera variavel de retorno
	my $R;
	my $R_;

	# print "<hr>$SQL<hr>";
	# sql exec
	$DB = $dbh->prepare($SQL);
	$DB->execute;
	if($dbh->err ne "") { &erroDBH($msg{db_select}." Lista de N.F. !!!"); &erroDBR; }		
	
	while($nf = $DB->fetchrow_hashref)
		{				
		# Data Ajusta
		$data_emissao_show = &dateToShow($nf->{data_emissao},"DATE"); # ajusta time stamp
		$data_vcto_show = &dateToShow($nf->{data_vcto},"DATE"); # ajusta time stamp
		
		# Cliente lenght
		if(length($nf->{cliente_nome}) > 50)
			{ $nf->{cliente_nome} = substr($nf->{cliente_nome}, 0, 50)."..."; }
			
		# Descrp lenght
		$nf->{descrp} = &get($nf->{descrp}, "NEWLINE_SHOW");
		if(length($nf->{descrp}) > 70)
			{ $nf->{descrp} = substr($nf->{descrp}, 0, 70)."...";  }
		
		$v_total = $nf->{vc1} + $nf->{vc2} + $nf->{vc3};
		$v_total = money($v_total);
		
		# $R_ .= "<tr class='days_ noglow noglow_' id='day_$nf->{codigo}' onClick=\\\"glow('day_$nf->{codigo}'); nfEditBtn($nf->{codigo});\\\" onDblClick='nfEdit($nf->{codigo})' style='cursor:pointer; height:23px;' class='$glow'><td style='text-align:center;'>$data_emissao_show </td><td style='text-align:center;'>$nf->{tempo_exec}</td><td style='padding-left:4px;'>$nf->{profissional_nome}</td><td style='padding-left:4px;'>$nf->{forma_descrp}</td><td style='padding-left:4px;'>$nf->{cliente_nome}</td><td style='padding-left:4px;'>$nf->{solicitante}</td><td style='padding-left:4px;'>$nf->{descrp} </td><td style='padding-left:4px; text-align:center;'>$nf->{servidor} </td></tr>";
        # glow($nf->{codigo});
		$R_ .= "<tr class='days_ noglow' id='day_$nf->{codigo}' onClick=\\\" nfEdit($nf->{codigo});\\\"  style='cursor:pointer; height:23px;'><td style='display:none;'>$nf->{codigo}</td><td style='padding-left:4px;'>$nf->{cliente_nome}</td><td style='text-align:center;'>$nf->{nf_num}</td><td style='text-align:center;'>$data_emissao_show</td><td style='text-align:center;'>$data_vcto_show</td><td style='padding-right:1%; text-align:right;'>$v_total</td></tr>";
		}
		
	# monta visualizacao	
	$R  = "<table id='$tb' cellspacing='1' cellpadding='1' class='navigateable grids' style='width:100%;'>";
	$R .= $THEAD;
	$R .= "	<tbody style='width:100%; '>";
	$R .= "	".$R_."";
	$R .= "	</tbody>";
	$R .= "</table>";	
	
	return $R;
	}

$R_month = &SQLNF($SQL_month, "nf_month_tb");
# $R_day = &SQLNF($SQL_day, "nf_day_tb");
# $R_all = &SQLNF($SQL_all, "nf_all_tb");

print "	
	<script>
		// \$(\"#nf_day\").html(\"$R_day\");
		\$(\"#nf_month\").html(\"$R_month\");
		// \$(\"#nf_all\").html(\"$R_all\");
		
		// \$(\".grids\").DGrid('bDestroy');
		// \$(\".grids\").DGrid();
		
		// new grid('nf_day_tb');
		// new grid('nf_month_tb');
		// new grid('nf_all_tb');
	</script>
	";



# [INI] NF PRINT CFG UPDATE ---------------------------------------------------------------------------------------------------
if($ACAO eq "cfg")
	{ #  = &get('cfg_left_');
	# $data_emissao_left = &get('cfg_left_data_emissao');
	# $data_top_left = &get('cfg_top_data_emissao');
	
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_data_emissao'))."', top='".(&get('cfg_top_data_emissao'))."' where descrp='data_emissao' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_nome'))."', top='".(&get('cfg_top_nome'))."' where descrp='nome' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_end'))."', top='".(&get('cfg_top_end'))."' where descrp='end' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_municipio'))."', top='".(&get('cfg_top_municipio'))."' where descrp='municipio' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_uf'))."', top='".(&get('cfg_top_uf'))."' where descrp='uf' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_cep'))."', top='".(&get('cfg_top_cep'))."' where descrp='cep' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_cnpj'))."', top='".(&get('cfg_top_cnpj'))."' where descrp='cnpj' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_ie'))."', top='".(&get('cfg_top_ie'))."' where descrp='ie' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_d1'))."', top='".(&get('cfg_top_d1'))."' where descrp='d1' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_v1'))."', top='".(&get('cfg_top_v1'))."' where descrp='v1' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_d2'))."', top='".(&get('cfg_top_d2'))."' where descrp='d2' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_v2'))."', top='".(&get('cfg_top_v2'))."' where descrp='v2' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_d3'))."', top='".(&get('cfg_top_d3'))."' where descrp='d3' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_v3'))."', top='".(&get('cfg_top_v3'))."' where descrp='v3' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_total'))."', top='".(&get('cfg_top_total'))."' where descrp='total' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_obs'))."', top='".(&get('cfg_top_obs'))."' where descrp='obs' ");
	$DB = $dbh->do("update nf_print set left_='".(&get('cfg_left_liquido'))."', top='".(&get('cfg_top_liquido'))."' where descrp='liquido' ");
	
	# sql exec
	# $DB = $dbh->do("update nf_print set data_emissao='$data_emissao', nome = '$nome', end = '$end', municipio = '$municipio', uf = '$uf', cep = '$cep', cnpj = '$cnpj', ie = '$ie', d1 = '$d1', v1 = '$v1', d2 = '$d2', v2 = '$v2', d3 = '$d3', v3 = '$v3', total = '$total', obs = '$obs', liquido = '$liquido'");
	
	# se erro
	if($dbh->err ne "") {  &erroDBH($msg{db_update}." N.F. CFG !!!");  $dbh->rollback;  &erroDBR;  exit; } #  se erro
	
	# logger
	# logger("nf","update","update nf set cliente=$cliente, data_emissao='$data_emissao', data_vcto='$data_vcto', nf_num='$nf_num', obs='$obs', d1='$d1', d2='$d2', d3='$d3', v1='$v1', v2='$v2', v3='$v3' where codigo = $COD");
	
	# exit;
	}
# [END] NF PRINT CFG UPDATE ---------------------------------------------------------------------------------------------------

# [INI] NF PRINT CFG -----------------------------------------------------------------------------------------------------
# sql exec
$DB = $dbh->prepare("select * from nf_print");
$DB->execute;

# se erro
if($dbh->err ne "") {  &erroDBH($msg{db_select}." N.F. CFG !!!");  $dbh->rollback;  &erroDBR; exit; } 

# popula variavel
while($nf_print = $DB->fetchrow_hashref)
	{
	# $print .= "\$('#cfg_left_$nf_print->{descrp}').css('width','60px').val('$nf_print->{left_}'); \$('#cfg_top_$nf_print->{descrp}').css('width','60px').val('$nf_print->{top}'); /* cfg_left_$nf_print->{descrp} = new fieldNumber('cfg_left_$nf_print->{descrp}', '4');  cfg_top_$nf_print->{descrp} = new fieldNumber('cfg_top_$nf_print->{descrp}', '4'); */";
	$print .= "\$('#cfg_left_$nf_print->{descrp}').css('width','60px').val('$nf_print->{left_}'); \$('#cfg_top_$nf_print->{descrp}').css('width','60px').val('$nf_print->{top}');";
	}
	
# retorno do script
print "<script>$print</script>";
# [END] NF PRINT CFG -----------------------------------------------------------------------------------------------------

exit;
