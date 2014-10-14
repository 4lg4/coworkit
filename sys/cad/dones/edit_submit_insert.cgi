#!/usr/bin/perl

$nacess = "999";
require "../../cfg/init.pl";
$ID = &get('ID');
$COD = &get('COD');
$MODO = &get('MODO');

$hostname = &get('hostname');
$usuario = &get('usuario');
$senha = &get('senha');
$descrp = &get('obs_user');
$domain = &get('dones_domains');
$domain_name = &get('domain_name');
$empresa = &get('empresa');
$endereco = &get('endereco');

$hostname=lc($hostname.".".$domain_name);

#[INI]/////////////////////////////////////////////////////////  Lembretes  ///////////////////////////////////////////////////////////////////#

# SELECT --> $DB1 = &DBE("select * from tabela where tabela is null order by campo");
# DELETE --> $DB2 = &DBE("delete from tabela where coluna='identificao'");
# INSERT --> $DB3 = &DBE("insert into tabela (campo1,campo2...) values ('".$variavel."') ");

#-------------------------------------------------------------------- While -------------------------------------------------------------------#

# while($row_title = $DB->fetchrow_hashref)
# 	{
# 	$modulos .="<li><a href='#t-$i'>$row_title->{'descrp'}</a></li>";
# 	$i++;
# 	}

#-------------------------------------------------------------------  FOR  --------------------------------------------------------------------#

#for($g=0; $g<$ncol; $g++)
# {
# $menu[$g] .= "<div class='menu menu_".$row->{'codigo'}."'>";
# }

#-----------------------------------------------  Pega o primeiro o id após inserção ou atualização -------------------------------------------#

# $codigo=$tipo_usuario->fetch;
# $DB4 = &DBE("update tabela set descrp='".ucfirstall($tipo_descrp)."' where codigo='@$codigo[0]'  ");

#--------------------------------------------  Recupera o ultida id cadastrado, somente após inserção  ----------------------------------------#

#[FIM]/////////////////////////////////////////////////////////  Lembretes  ///////////////////////////////////////////////////////////////////#

print $query->header({charset=>utf8});

if($usuario ne "")
	{
	#verifica se o usuario já existe
	$DB_ver = &DBE("select * from ti_users where usuario='".lc($usuario)."'");
	$rows=$DB_ver->rows();

	if($rows>0)
		{
		print "<script> alerta('O usuário já existe!');</script>";
		exit;
		}
	}
if($hostname ne "")
	{
	#verifica se o host já existe
	$DB_ver2 = &DBE("select * from ti_hosts where hostname='".lc($hostname)."'");
	$rows=$DB_ver2->rows();

	if($rows>0)
		{
		print "<script> alerta('O host já existe!'); </script>";
		exit;
		}
	}

################################################################################################################################################################

#Insere o usuario
$DB_users = &DBE("insert into ti_users (usuario,pwd,empresa,descrp,update_data,update_usuario) values ('$usuario','$senha','$empresa','$descrp',now(),$USER->{usuario})");

# recupera codigo inserido
$DB1 = &DBE("select currval('ti_users_codigo_seq')");
$row1 = $DB1->fetch;
$cod_user = @$row1[0];

################################################################################################################################################################

#Insere o host
$DB_hosts = &DBE("insert into ti_hosts (update_data,update_usuario,empresa,hostname) values (now(),$USER->{usuario},$empresa, '$hostname')");

# recupera codigo inserido
$DB2 = &DBE("select currval('ti_hosts_codigo_seq')");
$row2 = $DB2->fetch;
$cod_host = @$row2[0];

################################################################################################################################################################

$DB_dones = &DBE("insert into dones (data,ti_users,ti_hosts,empresa,endereco) values (now(),$cod_user,$cod_host,$empresa,$endereco)");

################################################################################################################################################################

print "	<script>
		unLoadingObj('bloco_form');
		proced_list('$endereco');
		DActionAdd();
		DMessages('Dones cadastrado com sucesso!');
	</script>";