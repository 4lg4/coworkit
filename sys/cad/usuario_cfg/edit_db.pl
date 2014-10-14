#!/usr/bin/perl

# Se ID Vazio redireciona para tela de login
if($ID eq "")
	{
	print $query->redirect("/");
	}

# Dados do usuário
if($COD ne "")
	{
	$DB = &DBE("select usuario.*, empresa.codigo as emp_codigo, empresa.nome as emp_nome from usuario left join empresa on usuario.empresa = empresa.codigo where usuario.usuario='$COD' ");
	while($row = $DB->fetchrow_hashref)
		{
		$login = $row->{'login'};
		$nome = $row->{'nome'};
		$email = $row->{'email'};
		$emp_codigo = $row->{'emp_codigo'};
		$emp_nome = $row->{'emp_nome'};
		$tipo_usuario_var = $row->{'tipo'};
		}
	}

# Tipos de Usuário
$DB = &select("select * from usuario_tipo order by descrp");
while($t = $DB->fetchrow_hashref)
	{
	# monta array com todos os itens para adicionar no radio
	$tipo_usuario .= "{val:$t->{codigo},descrp:'$t->{descrp}',img:'$t->{img}',},";
	}
$tipo_usuario = substr($tipo_usuario, 0,-1); # remove ultima virgula

# Pagina inicial
$DB = &DBE("select * from menu where codigo='46' or codigo='33' or codigo='43' or codigo='12'");
while($m = $DB->fetchrow_hashref)
	{
	# monta array com todos os itens para adicionar no radio
	$page_initial .= "{val:$m->{nacess},descrp:'$m->{descrp}', img:'$m->{icone}'},";
	}
$page_initial = substr($page_initial, 0,-1); # remove ultima virgula

# Quantidade de registro no grid
$grid .= "{val:'5',descrp:'5 Registros'},{val:'10',descrp:'10 Registros'},{val:'15',descrp:'15 Registros'}";

#se o usuario já tem configuração então faz os selecionamentos nos DTOUCH
$CFG_pg = &DBE("select * from usuario_cfg where usuario='$COD' and cfg=1 ");
$page_sel = $CFG_pg->fetchrow_hashref;

#se o usuario já tem configuração então faz os selecionamentos nos DTOUCH
$CFG_grid = &DBE("select * from usuario_cfg where usuario='$COD' and cfg=2 ");
$grid_sel = $CFG_grid->fetchrow_hashref;
	
return true;