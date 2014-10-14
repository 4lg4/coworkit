#!/usr/bin/perl

$nacess = 'nocheck';
require "../cfg/init.pl";

$ID = &get("ID");

print $query->header({charset=>utf8});

# [INI]  ID, Gera  ----------------------------------------------------------------------------------------------------------
if($ID eq "")
	{
	print $query->redirect("/");
	}
else
	{
	$rv = $dbh->do("update usuario_logado set ip = '$IP' where IP = '$RSITE' ");
	if($dbh->err ne "")
		{
		&erroDB("Falha em atualizar o log no Login!!!");
		}
	}
# [FIM]  ID, Gera  ----------------------------------------------------------------------------------------------------------

# [INI]  Menu Actions, get data from db  -----------------------------------------------------------------
$DB = $dbh->prepare("select * from menu where mobile != '' or mobile is not null order by descrp");
$DB->execute;
if($dbh->err ne "") {  &erroDBH($msg{db_select}." Menu Mobile !!!");  &erroDBR;  exit;  } # se erro
while($menu = $DB->fetchrow_hashref)
	{
	$Menu .= "<li data-theme='b'>";
    $Menu .= "	<a href='' data-transition='slide' onClick=\\\"$menu->{mobile}\\\">";
    $Menu .= "		$menu->{descrp}";
    $Menu .= "	</a>";
    $Menu .= "</li>";
	}
# [END]  Menu Actions, get data from db  -----------------------------------------------------------------

print<<HTML;

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

	<title>$nome_emp  - $nome_sys</title>
	<link rel="shortcut icon" href="/favicon.ico">
	
	<script src="/comum/DPAC_mobile.js"></script>

	<script>
	\$(document).ready(function() 
		{
		\$("#menu_mobile").html("$Menu").listview('refresh'); 
		
		// alert($ID);
		});
	</script>
</head>
<body>

<form name="mobile_frm" id="mobile_frm">
	<input type="hidden" name="ID" id="ID" value="$ID">
	<input type="hidden" name="MOBILE" id="MOBILE" value="MOBILE">
</form>

<div data-role="page" id="start_pg">
    <div data-theme="b" data-role="header">
        <h3>
            Dashboard
        </h3>
		<a data-role="button" data-transition="fade" data-theme="c"  data-icon="grid" data-iconpos="right" class="ui-btn-right" onClick="call('logon/logout.cgi')">
            Sair
        </a>
    </div>
    <div data-role="content" style="padding: 15px">
        <ul data-role="listview" data-divider-theme="b" data-inset="true" id="menu_mobile"></ul>
    </div>
</div>

</body>
</html>		
HTML
