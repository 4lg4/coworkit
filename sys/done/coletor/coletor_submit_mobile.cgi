#!/usr/bin/perl

$nacess = '66';
require "../cfg/init.pl";

print $query->header({charset=>utf8});

$ID = &get("ID");
$SEARCH = &get("SEARCH");
$EMP_COD = &get("EMP_COD");
$COLETOR = &get("COLETOR");

# print "<script>alert($EMP_COD = EMP_COD - $SEARCH = SEARCH')</script>";

# [INI]  Empresa View -------------------------------------------------------------------------------------------------------
if($EMP_COD ne "")
	{
	$DB = $dbh->prepare("select codigo, nome, apelido from empresa where codigo = $EMP_COD");
	$DB->execute;
	if($dbh->err ne "") {  &erroDBH($msg{db_select}." Empresa !!!");  &erroDBR;  exit;  } # se erro
	$empresa = $DB->fetchrow_hashref;
	
	# corrige se campo apelido estiver vazio
	if($empresa->{apelido} eq "")
		{ $empresa->{apelido} = substr($empresa->{nome}, 0, 15)."..."; }
	
	# gera lista de contatos telefonicos
	$DB = $dbh->prepare("select * from empresa_endereco where empresa = $EMP_COD");
	$DB->execute;
	if($dbh->err ne "") {  &erroDBH($msg{db_select}." Endereco !!!");  &erroDBR;  exit;  } # se erro
	while($endereco = $DB->fetchrow_hashref)
		{		
		# corrige se campo endereco para exibir no titulo
		$endereco_ = substr($endereco->{endereco}, 0, 15)."...";
		
		$enderecos .= "<div data-role='collapsible' data-collapsed='true' style='margin-top:5px;'>";
		$enderecos .= " 	<h3>End.: $endereco_</h3>";
		$enderecos .= " 	<div>";
		$enderecos .= " 	$endereco->{endereco} / $endereco->{complemento}<br>";
		$enderecos .= " 	$endereco->{bairro} / $endereco->{cidade} <br>";
		$enderecos .= " 	$endereco->{uf} / $endereco->{cep} <br>";
		$enderecos .= " 	</div>";
		$enderecos .= " </div>";
		}
		
	# retorno
	print "<script>
		\$('#emp_apelido').text('$empresa->{apelido}');
		// \$('#nome').val('$empresa->{nome}');
		// \$('#obs').text('$empresa->{obs}');
		// \$('#emp_contatos').html('$contatos').trigger('create');
		// \$('#emp_emails').html('$emails').trigger('create');
		// \$('#emp_end').html(\"$enderecos\").trigger('create');
		// \$('#coletor_view_pg').page();
		</script>";
	}
# [END]  Empresa View ------------------------------------------------------------------------------------------------------

# [INI]  Empresa List, get data from db  -----------------------------------------------------------------------------------
# se for pesquisa
if($SEARCH ne "")
	{ $SQL = "select codigo as emp_codigo, nome as emp_nome, apelido as emp_apelido from empresa where nome <=> '%".$SEARCH."%' or apelido <=> '%".$SEARCH."%'"; }
else
	{ $SQL = "select *, last_view.dt as lastdt from empresas_lista_distinct left join last_view on (empresas_lista_distinct.emp_codigo = last_view.codigo and last_view.tabela = 'empresa' and last_view.usuario = '".$USER->{usuario}."') limit 30"; }

$DB = $dbh->prepare($SQL);
$DB->execute;
if($dbh->err ne "") {  &erroDBH($msg{db_select}." Lista !!!");  &erroDBR;  exit;  } # se erro
while($list = $DB->fetchrow_hashref)
	{
	# corrige se campo apelido estiver vazio
	if($list->{emp_apelido} eq "")
		{ $list->{emp_apelido} = substr($list->{emp_nome}, 0, 15)."..."; }
		
	# gera lista	
	$List .= "<li data-theme='c'>";
    $List .= "	<a data-transition='slide' onClick=\\\"empresaView($list->{emp_codigo});\\\" id='emp_$list->{emp_codigo}'>";
    $List .= "		$list->{emp_apelido}";
    $List .= "	</a>";
    $List .= "</li>";
	}
	
# retorno
# print "<script>\$(\"#list_mobile\").html(\"$List\").listview('refresh');</script>";
print "<script>\$(\"#list_mobile\").html(\"$List\");</script>";
# [END]  Empresa List, get data from db  -----------------------------------------------------------------------------------

# [INI]  Coletores  --------------------------------------------------------------------------------------------------------
# sql exec
$DB = $dbh->prepare("select coletor.*, usuario.nome as profissional_nome, coletor_forma.descrp as forma_descrp, empresa.nome as nome, empresa.apelido as apelido from coletor left join usuario on (usuario.usuario = coletor.profissional) left join coletor_forma on (coletor_forma.codigo = coletor.forma) left join empresa on (empresa.codigo = coletor.cliente) where profissional = '$USER->{usuario}' order by coletor.data_exec asc limit 20");
$DB->execute;
if($dbh->err ne "") { &erroDBH($msg{db_select}." Lista de Coletores !!!"); &erroDBR; }		

while($coletor = $DB->fetchrow_hashref)
	{				
	# Data Ajusta
	$data_exec_show = &dateToShow($coletor->{data_exec},"DATE"); # ajusta time stamp		
	
	# Hora servidor 
	if($coletor->{servidor} == 0)
		{ $coletor->{servidor} = "Não"; }
	else
		{ $coletor->{servidor} = "<b>Sim</b>"; }
	
	# Cliente lenght
	if(length($coletor->{cliente_nome}) > 30)
		{ $coletor->{cliente_nome} = substr($coletor->{cliente_nome}, 0, 30)."..."; }
		
	# Profissional lenght
	if(length($coletor->{profissional_nome}) > 20)
		{ $coletor->{profissional_nome} = substr($coletor->{profissional_nome}, 0, 20)."..."; }
	
	# Solicitante lenght
	if(length($coletor->{solicitante}) > 20)
		{ $coletor->{solicitante} = substr($coletor->{solicitante}, 0, 20)."..."; }
		
	# Descrp lenght
	if(length($coletor->{descrp}) > 70)
		{ $coletor->{descrp} = substr($coletor->{descrp}, 0, 70)."..."; }
		
	# Cliente lenght
	if($coletor->{apelido} eq "")
		{ $coletor->{apelido} = substr($coletor->{nome}, 0, 10)."..."; }
	# $R_ .= "<tr class='days_ noglow noglow_' id='day_$coletor->{codigo}' onClick=\\\"glow('day_$coletor->{codigo}'); coletorEditBtn($coletor->{codigo});\\\" onDblClick='coletorEdit($coletor->{codigo})' style='cursor:pointer; height:23px;' class='$glow'><td style='text-align:center;'>$data_exec_show </td><td style='text-align:center;'>$coletor->{tempo_exec}</td><td style='padding-left:4px;'>$coletor->{profissional_nome}</td><td style='padding-left:4px;'>$coletor->{forma_descrp}</td><td style='padding-left:4px;'>$coletor->{cliente_nome}</td><td style='padding-left:4px;'>$coletor->{solicitante}</td><td style='padding-left:4px;'>$coletor->{descrp} </td><td style='padding-left:4px; text-align:center;'>$coletor->{servidor} </td></tr>";
	# $R_ .= "<tr class='days_ noglow' id='day_$coletor->{codigo}' onClick=\\\"glow($coletor->{codigo}); coletorEdit($coletor->{codigo});\\\"  style='cursor:pointer; height:23px;'><td style='text-align:center;'>$data_exec_show </td><td style='text-align:center;'>$coletor->{tempo_exec}</td><td style='padding-left:4px;'>$coletor->{profissional_nome}</td><td style='padding-left:4px;'>$coletor->{forma_descrp}</td><td style='padding-left:4px;'>$coletor->{cliente_nome}</td><td style='padding-left:4px;'>$coletor->{solicitante}</td><td style='padding-left:4px;'>$coletor->{descrp} </td><td style='padding-left:4px; text-align:center;'>$coletor->{servidor} </td></tr>";
	# gera lista	
	$ListC .= "<li data-theme='c'>";
    $ListC .= "	<a data-transition='slide' onClick=\\\"coletorView($coletor->{codigo});\\\">";
    $ListC .= "		".(&dateToShow($coletor->{data_exec},"DATE"))." / $coletor->{tempo_exec} - $coletor->{apelido}";
    $ListC .= "	</a>";
    $ListC .= "</li>";
	}

# retorno
print "<script>\$(\"#list_coletor_mobile\").html(\"$ListC\");</script>";
# [END]  Coletores  --------------------------------------------------------------------------------------------------------

# print "<script>\$(\"#list_mobile\").listview('refresh');</script>";
# // print "<script>\$(\"#list_coletor_mobile\").trigger('create');</script>";
# print "<script>\$('ul').listview('refresh');</script>";
# exit;

# [INI]  Coletor View  -----------------------------------------------------------------------------------------------------
if($COLETOR ne "")
	{
	# sql exec
	$DB = $dbh->prepare("select coletor.*, usuario.nome as profissional_nome, coletor_forma.descrp as forma_descrp, empresa.nome as nome, empresa.apelido as apelido from coletor left join usuario on (usuario.usuario = coletor.profissional) left join coletor_forma on (coletor_forma.codigo = coletor.forma) left join empresa on (empresa.codigo = coletor.cliente) where coletor.codigo = $COLETOR");
	$DB->execute;
	if($dbh->err ne "") { &erroDBH($msg{db_select}." Lista de Coletores !!!"); &erroDBR; }		

	$coletor = $DB->fetchrow_hashref;
	# while($coletor = $DB->fetchrow_hashref)
		# {				
		# Data Ajusta
		# $data_exec_show = &dateToShow($coletor->{data_exec},"DATE"); # ajusta time stamp		
	
		# Hora servidor 
		if($coletor->{servidor} == 0)
			{ $coletor->{servidor} = "Não"; }
		else
			{ $coletor->{servidor} = "<b>Sim</b>"; }
	
		# Cliente lenght
		if(length($coletor->{cliente_nome}) > 30)
			{ $coletor->{cliente_nome} = substr($coletor->{cliente_nome}, 0, 30)."..."; }
		
		# Profissional lenght
		if(length($coletor->{profissional_nome}) > 20)
			{ $coletor->{profissional_nome} = substr($coletor->{profissional_nome}, 0, 20)."..."; }
	
		# Solicitante lenght
		if(length($coletor->{solicitante}) > 20)
			{ $coletor->{solicitante} = substr($coletor->{solicitante}, 0, 20)."..."; }
		
		# Descrp lenght
		if(length($coletor->{descrp}) > 70)
			{ $coletor->{descrp} = substr($coletor->{descrp}, 0, 70)."..."; }
		
		# Cliente lenght
		if($cliente->{apelido} eq "")
			{ $cliente->{apelido} = substr($cliente->{nome}, 0, 10)."..."; }
		# $R_ .= "<tr class='days_ noglow noglow_' id='day_$coletor->{codigo}' onClick=\\\"glow('day_$coletor->{codigo}'); coletorEditBtn($coletor->{codigo});\\\" onDblClick='coletorEdit($coletor->{codigo})' style='cursor:pointer; height:23px;' class='$glow'><td style='text-align:center;'>$data_exec_show </td><td style='text-align:center;'>$coletor->{tempo_exec}</td><td style='padding-left:4px;'>$coletor->{profissional_nome}</td><td style='padding-left:4px;'>$coletor->{forma_descrp}</td><td style='padding-left:4px;'>$coletor->{cliente_nome}</td><td style='padding-left:4px;'>$coletor->{solicitante}</td><td style='padding-left:4px;'>$coletor->{descrp} </td><td style='padding-left:4px; text-align:center;'>$coletor->{servidor} </td></tr>";
		# $R_ .= "<tr class='days_ noglow' id='day_$coletor->{codigo}' onClick=\\\"glow($coletor->{codigo}); coletorEdit($coletor->{codigo});\\\"  style='cursor:pointer; height:23px;'><td style='text-align:center;'>$data_exec_show </td><td style='text-align:center;'>$coletor->{tempo_exec}</td><td style='padding-left:4px;'>$coletor->{profissional_nome}</td><td style='padding-left:4px;'>$coletor->{forma_descrp}</td><td style='padding-left:4px;'>$coletor->{cliente_nome}</td><td style='padding-left:4px;'>$coletor->{solicitante}</td><td style='padding-left:4px;'>$coletor->{descrp} </td><td style='padding-left:4px; text-align:center;'>$coletor->{servidor} </td></tr>";
		# gera lista	
		# $List .= "<li data-theme='c'>";
	    # $List .= "	<a data-transition='slide' onClick=\\\"coletorView($coletor->{codigo});\\\">";
	    # $List .= "		".(&dateToShow($coletor->{data_exec},"DATE"))." / $coletor->{tempo_exec} / $coletor->{apelido}";
	    # $List .= "	</a>";
	    # $List .= "</li>";
		# }

	# retorno
	print "<script>
				\$('#emp_apelido').text('$coletor->{apelido}');
				\$('#data_exec').val('".(&dateToShow($coletor->{data_exec},"DATE"))."');
				\$('#tempo_exec').val('$coletor->{tempo_exec}');
				\$('#emp_apelido').text('$coletor->{apelido}');
			</script>";
	}
# [END]  Coletor View  -----------------------------------------------------------------------------------------------------


print "<script>\$('ul').listview('refresh');</script>";
exit;