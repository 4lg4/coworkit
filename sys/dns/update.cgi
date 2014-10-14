#!/usr/bin/perl

use URI::Escape;

$ID = "";
require "../cfg/init.pl";

$username = $ENV{'REMOTE_USER'};
$hostname = &get('hostname');
$myip = &get('myip');


print "Content-type: text/plain; charset='UTF-8'\n\n";

$result = "Valores Recebidos: ";
@campo = $query->param();
for($f=0;$f<@campo;$f++)
	{
	$result .= $campo[$f].": ".&get($campo[$f])."\n";
	}


if($username ne "")
	{
	$rv = $dbh->do("insert into dns_historico (usuario, host, ip, ip_real, dt) values ('$username', '$hostname', '$myip', '$IP', now())");
	if($dbh->err ne "")
		{
		print "dnserr\n".$dbh->errstr."\n";
		}
	else
		{
		$sth2 = $dbh->prepare("select * from dns_done where usuario = '$username' and host = '$hostname' ");
		$sth2->execute();
		if($dbh->err ne "")
			{
			print "dnserr\n".$dbh->errstr."\n";
			}
		$rv2 = $sth2->rows();
		if($rv2 > 0)
			{
			$rv = $dbh->do("update dns_done set ip_real = '$IP', ip_informado = '$myip' where usuario = '$username' and host = '$hostname' ");
			if($dbh->err ne "")
				{
				print "dnserr\n".$dbh->errstr."\n";
				}
			else
				{
				if($rv == 0)
					{
					print "nochg $IP";
					}
				else
					{
					print "good $IP";
					}
				}
			}
		else
			{
			print "nohost";
			}
		}
	}
else
	{
	print "badauth";
	}

