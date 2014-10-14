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

$DB_COD = &DBE("select * from dones where codigo=$COD");
$row_cod = $DB_COD->fetchrow_hashref;

################################################################################################################################################################

#deleta o usuario
$DB_users = &DBE("delete from ti_users where codigo=$row_cod->{ti_users}");

################################################################################################################################################################

#Insere o host
$DB_hosts = &DBE("delete from ti_hosts where codigo=$row_cod->{ti_hosts}");

################################################################################################################################################################

$DB_dones = &DBE("delete  from dones where codigo=$COD");

################################################################################################################################################################

print "	<script>
		unLoadingObj('bloco_form');
		proced_list('$endereco');
		DActionAdd();
		DMessages('Dones deletado com sucesso!');
	</script>";