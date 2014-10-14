###############################################
# Script Desenvolvido por Kelvyn Carbone      #
# 					      #
# Script para importação de dados do done DNS #
# #############################################

#!/usr/bin/perl

$nacess = "999";
require "../../cfg/init.pl"; #ou "../cfg/init.pl"

$ID = &get('ID');
$COD = &get('COD');
$MODO = &get('MODO');

print $query->header({charset=>utf8});

# Puxa todos os dones
$DB_DNS = DBE("select empresa,endereco,usuario,senha,host from dns_done");

while($dns=$DB_DNS->fetchrow_hashref)
	{
	#Insere o usuario
	$DB_USER= DBE("insert into ti_users (usuario,pwd,empresa,update_data,update_usuario)
			values ('$dns->{usuario}','$dns->{senha}','$dns->{empresa}',now(),1) ");
			
	# recupera codigo inserido do usuario
	$COD_USER = &DBE("select currval('ti_users_codigo_seq')");
	$row1 = $COD_USER->fetch;
	$cod_user = @$row1[0];
	
	#Insere o host
	$DB_USER= DBE("insert into ti_hosts (update_data,update_usuario,empresa,hostname)
			values ('now()',1,'$dns->{empresa}','$dns->{host}') ");
			
	# recupera codigo inserido do usuario
	$COD_HOST = &DBE("select currval('ti_hosts_codigo_seq')");
	$row2 = $COD_HOST->fetch;
	$cod_host = @$row2[0];
	
	#Insere o dones
	$DB_USER= DBE("insert into dones (data,ti_users,ti_hosts,empresa,endereco)
			values (now(),$cod_user,$cod_host,$dns->{empresa},$dns->{endereco}) ");
	
	}

print "<script> alerta('Dados importados com sucesso!');</script>"