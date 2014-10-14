#!/usr/bin/perl

$nacess = 'nocheck';
require "../../cfg/init.pl";

$usuario = &get('usuario');
$usuario_tipo = &get('tipo');

print "Content-type: text/html\n\n";
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
HTML

$sth = &select("select max(codigo)/1000 from menu");
while($row = $sth->fetch)
	{
	$ncol = @$row[0]+1;
	}
$sth->finish;

$SQL3 = "select * from tipo_direito where codigo ilike 'v' or codigo ilike 'a' order by descrp";
$sth3 = &select($SQL3);
$rv3 = $sth3->rows();
$tipo_direito_list = "";
if($rv3 < 1)
	{
	$tipo_direito_list .= "<option value=''>Nenhum tipo de direito cadastrado</option>";
	}
else
	{
	$c = 0;
	while($row3 = $sth3->fetchrow_hashref)
		{
		# $tipo_cod[$c] = $row3->{'codigo'};
		$tipo_cod[$c] = $row3->{'nacess'};
		# $tipo_nacess[$c] = $row3->{'nacess'};
		$tipo_descr[$c] = $row3->{'descrp'};
		$c++;
		}
	}
$sth3->finish;

$sth = &select("select max(codigo)/1000 from menu");
while($row = $sth->fetch)
	{
	$ncol = @$row[0]+1;
	}
$sth->finish;


$sth = &select("select * from menu where pai is null order by ordem");
$rv = $sth->rows();
if($rv < 1)
	{
print<<HTML;
</div>
<div style='position: absolute; top: 50%; width: 100%;'>
	<center><span id='bemvindo_titulo'>Por favor contacte o administrador para solicitar seu acesso</span></center>
</div>
HTML
	}
else
	{
	while($row = $sth->fetchrow_hashref)
		{
		&get_direitos($row->{'codigo'});
		@menu = ("");
		for(my $g=0; $g<$ncol; $g++)
			{
			$menu[$g] .= "<div class='menu menu_".$row->{'codigo'}."'>";
			}

		print "<div style='position: relative;'><ul><li class='submenu'><span id='menu_text'>";
		print $row->{'descrp'};
		if($row->{'acao'} ne "")
			{
			print "<div style='width: 260px;'><select name='".$row->{codigo}."' style='float: right; position: relative; top: -17px;'>";
			print "<option value=''>Sem acesso</option>";

			$SQL3 = "select * from tipo_direito join menu_tipo_direito on tipo_direito.codigo = menu_tipo_direito.tipo_direito where menu_tipo_direito.menu = '$row->{nacess}' order by descrp";
			# debug($SQL3);
			
			$sth3 = &select($SQL3);
			$rv3 = $sth3->rows();
			$tipo_direito_list = "";
			if($rv3 < 1)
				{
				for($f=0; $f<@tipo_cod; $f++)
					{
					print "<option value='".$tipo_cod[$f]."' ";
					if($tipo_cod[$f] eq $tipo_sel)
						{
						print "selected";
						}
					print ">".$tipo_descr[$f]."</option>"
					}
				}
			else
				{
				while($row3 = $sth3->fetchrow_hashref)
					{
					print "<option value='".$row3->{'codigo'}."' ";
					if($row3->{'codigo'} eq $tipo_sel)
						{
						print "selected";
						}
					print ">".$row3->{'descrp'}."</option>"
					}
				}
			print "</select></div>";
			}
		print "</span>";
		&get_menu($row->{'codigo'});

		for(my $g=0; $g<$ncol; $g++)
			{
			$menu[$g] .= "</div>";
			}

		$cell=0;
		print "</li></ul><table border=0 cellpadding=0 cellspacing=0><tr valign=top>";
		for($f=0; $f<@menu; $f++)
			{
			print "<td width=280 style='padding-right: 50px'>";
			if($f>0)
				{
				print "<ul>";
				}
			print $menu[$f];
			if($f>0)
				{
				print "</ul>";
				}
			print "</div>\n";
			print "</td>";
			}
		print "</tr></table>";

		print "</div>";

		}
	}

print<<HTML;
<br clear=both><br>
</body></html>
HTML


exit;

















sub get_menu
	{
	my ($pai) = @_;
	my $SQL = "";
	if($pai eq "")
		{
		return;
		}

	$SQL = "select * from menu where pai = '$pai' order by ordem ";
	my $sth = &select($SQL);
	my $rv = $sth->rows();
	if($rv > 0)
		{
		$menu[int($pai/1000)] .= "<ul>";
		while(my $row = $sth->fetchrow_hashref)
			{ # debug($row->{'codigo'}." - ".$row->{'nacess'});
			&get_direitos($row->{'codigo'});
			my $pos = 0;
			if($row->{'codigo'} > $pai)
				{
				$pos = int($row->{'codigo'}/1000);
				}
			else
				{
				$pos = int($pai/1000);
				}
			if($row->{'acao'} ne "")
				{
				$menu[$pos] .= "<li><a>$row->{'descrp'}</a>";
				$menu[$pos] .= "<select name='".$row->{codigo}."' style='float: right; position: relative; top: -17px;'>";
				$menu[$pos] .= "<option value=''>Sem acesso</option>";

				$SQL3 = "select * from tipo_direito join menu_tipo_direito on tipo_direito.codigo = menu_tipo_direito.tipo_direito where menu_tipo_direito.menu = '$row->{nacess}' order by descrp";
				# debug($SQL3);
				
				$sth3 = &select($SQL3);
				$rv3 = $sth3->rows();
				$tipo_direito_list = "";
				if($rv3 < 1)
					{
					for($f=0; $f<@tipo_cod; $f++)
						{
						$menu[$pos] .= "<option value='".$tipo_cod[$f]."' ";
						if($tipo_cod[$f] eq $tipo_sel)
							{
							$menu[$pos] .= "selected";
							}
						$menu[$pos] .= ">".$tipo_descr[$f]."</option>"
						}
					}
				else
					{
					while($row3 = $sth3->fetchrow_hashref)
						{
						$menu[$pos] .= "<option value='".$row3->{'codigo'}."' ";
						if($row3->{'codigo'} eq $tipo_sel)
							{
							$menu[$pos] .= "selected";
							}
						$menu[$pos] .= ">".$row3->{'descrp'}."</option>"
						}
					}
				$menu[$pos] .= "</select></li><br>";
				}
			else
				{
				if($menu[$pos] =~ /li/)
					{
					$menu[$pos] .= "<br>";
					}
				$menu[$pos] .= "<li class='submenu'>$row->{'descrp'}</li>";
				}
			&get_menu($row->{'codigo'});
			}
		$menu[int($pai/1000)] .= "</ul>";
		}
	return;
	}

sub get_direitos
	{
	my ($cod) = @_;
	if($cod eq "")
		{
		return;
		}

	if($usuario eq "admin" || $usuario_tipo eq "1")
		{
		$tipo_sel = "a";
		}
	elsif($usuario_tipo ne "")
		{
		$tipo_sel = "";
		$sth42 = &select("select * from menu_default_direitos where usuario_tipo = '$usuario_tipo' and menu = '$cod' limit 1");
		$rv42 = $sth42->rows();
		if($rv42 > 0)
			{
			while($row42 = $sth42->fetchrow_hashref)
				{
				$tipo_sel = $row42->{'tipo'};
				}
			}
		}
	elsif($usuario ne "")
		{
		$tipo_sel = "";
		$sth42 = &select("select * from usuario_menu where usuario = '$usuario' and menu = '$cod' limit 1");
		$rv42 = $sth42->rows();
		if($rv42 > 0)
			{
			while($row42 = $sth42->fetchrow_hashref)
				{
				$tipo_sel = $row42->{'tipo'};
				}
			}
		}
	}


