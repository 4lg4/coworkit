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
	
return true;