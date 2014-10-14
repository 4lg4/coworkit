#!/usr/bin/perl

$nacess = 'nocheck';
require "../cfg/init.pl";

# suporte para login mobile
$MOBILE = &get("MOBILE");

if($ID eq "" && $ENV{'QUERY_STRING'} ne "")
	{
	$buffer = $ENV{'QUERY_STRING'};
	# Split information into name/value pairs
	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs)
		{
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%(..)/pack("C", hex($1))/eg;
		$FORM{$name} = $value;
		}
	$ID = $FORM{ID};
	}

if($ID ne "")
	{
	# Rotina de logout
	$dbh->begin_work;
	$rv = $dbh->do("insert into usuario_historico (usuario, empresa, dt, ip, req) select usuario, empresa, ini, ip, 'Saiu' from usuario_logado where ID = '$ID' ");
	if($dbh->err ne "")
		{
		print $query->header({charset=>utf8});
		&erroDBH("Falha no Logout!!!");
		$dbh->rollback;
		}
	if($rv > 0)
		{
		$rv = $dbh->do("delete from usuario_logado where ID = '$ID' ");
		}
	if($dbh->err ne "")
		{
		print $query->header({charset=>utf8});
		&erroDBH("Falha no Logout!!!");
		$dbh->rollback;
		}
	$dbh->commit;
	}

# Apaga acessos inativos
$rv = $dbh->do("delete from usuario_logado where now() > (FIM + interval '$timeout seconds' + interval '1 day') ");
if($dbh->err ne "")
	{
	print $query->header({charset=>utf8});
	&erroDB("Falha no Logout!!!");
	$dbh->rollback;
	}


# Volta a tela inicial
# suporte para login mobile
if($MOBILE ne "")
	{ print $query->redirect("/m/"); }
else
	{ print $query->redirect("/"); }
