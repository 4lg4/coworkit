#!/usr/bin/perl

use utf8;
use HTML::Entities;
use Encode;

$ID = "";
require "../cfg/init.pl";

$vers = 'Ver. 20130318';

$codigo = &get('codigo');
$chave = &get('chave');
$descrp = decode_entities(&get(descrp));
$item = &get(item);
$valor = &get(valor);
$max = &get(max);
if($max eq "")
	{
	$max = NULL;
	}
	
# Se não for UTF-8 válido, assume ISO-8859-1
my $encoding = detect_utf8(\$descrp) ? 'utf8' : 'iso-8859-1';
if($encoding eq 'iso-8859-1')
	{
	# Processa a codificação
	$descrp = decode($encoding, $descrp);
	}

print "Content-type: text/plain; charset='UTF-8'\n\n";

#print "Código: $codigo\n";
#print "Chave: $chave\n";
#print "Descrp: $descrp\n";
#print "Valor: $valor\n";

if($codigo ne "" && $valor ne "")
	{
	$SQL = "select *, empresa_endereco.empresa as cod_emp, empresa_endereco.codigo as cod_end from monitor_grupo left join empresa_endereco on monitor_grupo.endereco = empresa_endereco.codigo where monitor_grupo.codigo = '$codigo' ";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv > 0)
		{
		while($row = $sth->fetchrow_hashref)
			{
			#print "Empresa: ".$row->{'nome_emp'}." (".$row->{'cod_emp'}.")\n";
			if($row->{'chave'} eq $chave)
				{
				$rv = $dbh->do("insert into monitor_historico (monitor, dt, ip, descrp, item, valor, valor_max) values ('$codigo', now(), '$IP', '$descrp', '$item', '$valor', '$max') ");
				if($dbh->err ne "")
					{
					print "Erro!\n".&get($dbh->errstr,"NEWLINE_SHOW")."\n";
					print $vers;
					}
				else
					{
					print "OK!\n";
					print $vers;
					}
				}
			else
				{
				print "Requisição negada!\n";
				}
			}
		}
	}
else
	{
	print "Acesso negado!\n";
	}


# detect_utf8(\$string)
# Recebe referência para escalar com string a ser analisada e retorna:
# 0 - $string tem caracteres de 8 bits, não valida como UTF-8;
# 1 - $string tem somente caracteres de 7 bits;
# 2 - $string tem caracteres de 8 bits, valida como UTF-8.
# Algoritmo original em PHP: http://www.php.net/manual/en/function.utf8-encode.php#85293
# Fórmula da conversão: http://home.tiscali.nl/t876506/utf8tbl.html#algo
 sub detect_utf8
	{
	use bytes;

	my $str = shift;
	my $d = 0;
	my $c = 0;
	my $b = 0;
	my $bits = 0;
	my $len = length ${$str};

	for (my $i = 0; $i < $len; $i++)
		{
		$c = ord(substr(${$str}, $i, 1));
		if($c >= 128)
			{
			$d++;

			if($c >= 254)
				{
				return 0;
				}
			elsif($c >= 252)
				{
				$bits = 6;
				}
			elsif($c >= 248)
				{
				$bits = 5;
				}
			elsif($c >= 240)
				{
				$bits = 4;
				}
			elsif($c >= 224)
				{
				$bits = 3;
				}
			elsif($c >= 192)
				{
				$bits = 2;
				}
			else
				{
				return 0;
				}
			if(($i + $bits) > $len)
				{
				return 0;
				}

			while ($bits > 1)
				{
				$i++;
				$b = ord(substr(${$str}, $i, 1));
				if(($b < 128) || ($b > 191))
					{
					return 0;
					}
				$bits--;
				}
			}
		}

	return $d ? 2 : 1;
	}
