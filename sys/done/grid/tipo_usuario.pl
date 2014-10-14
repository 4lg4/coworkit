$GRUPO = &get("GRUPO"); # pega dado do select grupos relacionados do formulario em start.cgi
$qtdcmp = 6;

$cfg_2 = &get_cfg(2);
if(&get_cfg(2) eq "")
	{
	$cfg_2 = "10"; # se vazio define numero minimo de linhas que sao mostradas
	}

if($ORDER eq "")
	{
	$ORDER = "last"; # se vazio define qual campo sera a chave da ordenacao
	}
print<<END;
<div id="grid_scroll" style="clear: both">
<table width=100% border=0 cellpadding=4 cellspacing=0 class="navigateable" id="grid">
	<thead>
		<tr>
END

print "			<th id='codigo' width=5% onClick=\"orderby('codigo')\"";
if($ORDER eq "codigo")
	{
	print " class='asc'";
	}
elsif($ORDER eq "codigo desc")
	{
	print " class='desc'";
	}
else
	{
	print " class='thor'";
	}
print ">Código</th>\n";

print "			<th id='descricao' width=95% onClick=\"orderby('descricao')\"";
if($ORDER eq "descricao")
	{
	print " class='asc'";
	}
elsif($ORDER eq "contato desc")
	{
	print " class='desc'";
	}
else
	{
	print " class='thor'";
	}
print ">Descrição</th>\n";

	


print<<END;
		</tr>
	</thead>
	<tbody>
END

$SQL = "select * from usuario_tipo where descrp is not null ";

if($CAMPO ne "" && ($PESQLETRA ne "" || $PESQ ne ""))
	{
	if($CAMPO eq "Código")
		{
		$CAMPO = "codigo";
		}
	elsif($CAMPO eq "Descrição")
		{
		$CAMPO = "descrp";
		}

	if($CAMPO eq "codigo")
		{
		$SQL .= " and ".$CAMPO;
		if($PESQLETRA ne "")
			{
			if($PESQLETRA =~ /[a-zA-Z]/)
				{
				$SQL .= " = '0' ";
				}
			elsif($PESQLETRA eq "#")
				{
				$SQL .= " > 0 ";
				}
			else
				{
				$SQL .= " = '$PESQLETRA' ";
				}
			}
		else
			{
			$SQL .= " = ";
			if($PESQ =~ /[a-zA-Z]/)
				{
				$SQL .= " '0' ";
				}
			else
				{
				$SQL .= " '$PESQ' ";
				}
			}
		}
	else
		{
		$SQL .= " and ".$CAMPO;
		if($PESQLETRA eq "#")
			{
			$SQL .= " ~ '(^[0-9])' ";
			}
		elsif($PESQLETRA ne "")
			{
			$SQL .= " <=> '%$PESQLETRA%' ";
			}
		elsif($PESQ ne "")
			{
			$SQL .= " <=> '%$PESQ%' ";
			}
		}
	}
else
	{
	if($PESQLETRA eq "#")
		{
		$SQL .= " and descrp ~ '(^[0-9])' ";
		}
	elsif($PESQLETRA ne "")
		{
		$SQL .= " and (descrp <=> '%$PESQLETRA%') ";
		}
	elsif($PESQ ne "")
		{
		$SQL .= " and (descrp <=> '%$PESQ%') ";
		}
	}

if($ORDER eq "codigo")
	{
	$SQL .= "order by codigo";
	}
elsif($ORDER eq "codigo desc")
	{
	$SQL .= "order by codigo desc";
	}
elsif($ORDER eq "descricao")
	{
	$SQL .= "order by descrp";
	}
elsif($ORDER eq "descricao desc")
	{
	$SQL .= "order by descrp desc";
	}
else
	{
	$SQL .= "order by codigo, descrp ";
	}

$sth = &select($SQL);
$rv = $sth->rows();
if($rv < 1)
	{
print<<END;
	<tr>
		<td colspan=5>Nenhum registro encontrado</td>
	</tr>
END
	}
else
	{
	while($row = $sth->fetchrow_hashref)
		{
print<<END;
		<tr id='$row->{'codigo'}' onDblClick='view("$row->{'codigo'}")' onClick='pre_view("$row->{'codigo'}")'>
			<td title='$row->{'codigo'}'>$row->{'codigo'}</td>
			<td title='$row->{'descrp'}'>$row->{'descrp'}</td>
		</tr>
END
		}
	}
print<<END;
	</tbody>
</table>
</div>
END
