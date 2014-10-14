#!/usr/bin/perl

$nacess = "207";
require "../../cfg/init.pl"; #ou ../cfg/init.pl
$ID = &get('ID');
$COD = &get('COD');
$MODO = &get('MODO');

$user = &get('username');
$hostname = &get('hostname');

print $query->header({charset=>utf8});

if($user ne "")
	{
	#verifica se o usuario já existe
	$DB1 = &DBE("select * from ti_users where usuario='".lc($user)."'");
	$rows=$DB1->rows();

	if($rows>0)
		{
		print "1";
		}
	else
		{
		print "0";
		}
	}
elsif($hostname ne "")
	{
	#verifica se o host já existe
	$DB1 = &DBE("select * from ti_hosts where hostname='".lc($hostname)."'");
	$rows=$DB1->rows();

	if($rows>0)
		{
		print "1";
		}
	else
		{
		print "0";
		}
	}