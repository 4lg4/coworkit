#!/usr/bin/perl


$nacess = 'nocheck';
require "../cfg/init.pl";
$USER{USUARIO} = &get("username");
$SENHA = &get("password");
$USER{EMPRESA} = &get("empresa");
$ID = &get("ID");
$COD = &get("COD");
$IP = $ENV{'REMOTE_ADDR'};
$THIS = &get("THIS");

# suporte para login mobile
$MOBILE = &get("MOBILE");

print $query->header({charset=>utf8});

print "<form name='login' id='login' target='main' method='POST' action='$THIS'>\n";
@campo = $query->param();
for($f=0;$f<@campo;$f++)
	{
	print "<input type='hidden' name='".$campo[$f]."' value='".&get($campo[$f])."'>\n";
	}
print "</form>\n";


print "<script language='JavaScript'>";
require "./login_db.pl";

$ID = &check_login;
if($ID ne "")
	{
print<<HTML;
	try
		{
		top.document.forms[0].ID.value = "$ID";
		document.forms[0].ID.value = "$ID";
		}
	catch(err)
		{
		document.forms[0].ID.value = "$ID";		
		}
	
	blastcall = false;
	reloginoff();
	if(slastcall != "")
		{
		eval(slastcall);
		slastcall="";
		}
HTML
	}
print "</script>";
exit;
	
