#!/usr/bin/perl

$nacess = "999";
require "../../cfg/init.pl";
$ID = &get('ID');
$COD = &get('COD');
$MODO = &get('MODO');

$hostname = &get('hostname');
$usuario = &get('usuario');
$senha = &get('senha');
$user_verifica = &get('user_verifica');
$host_verifica = &get('host_verifica');
$descrp = &get('obs_user');
$domain = &get('dones_domains');
$domain_name = &get('domain_name');
$empresa = &get('empresa');
$endereco = &get('endereco');

$hostname=lc($hostname.".".$domain_name);

$host_verifica=lc($host_verifica.".".$domain_name);


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


if($usuario ne "" && $usuario ne $user_verifica)
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
if($hostname ne "" && $hostname ne $host_verifica)
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

$DB_COD = &DBE("select * from dones where codigo=$COD");
$row_cod = $DB_COD->fetchrow_hashref;

################################################################################################################################################################

#deleta o usuario
$DB_users = &DBE("update ti_users set usuario='$usuario', pwd='$senha', descrp='$descrp', update_data=now(), update_usuario='$USER->{usuario}' where codigo=$row_cod->{ti_users}");

################################################################################################################################################################

#deleta o usuario
$DB_hosts = &DBE("update ti_hosts set hostname='$hostname', update_data=now(), update_usuario='$USER->{usuario}' where codigo=$row_cod->{ti_hosts}");

################################################################################################################################################################

$DB_dones = &DBE("update dones set data=now(), endereco='$endereco' where codigo=$COD");


################################################################################################################################################################

print "	<script>
		unLoadingObj('bloco_form');
		proced_list('$endereco');
		DActionCancel();
		DMessages('Dones atualizado com sucesso!');
	</script>";