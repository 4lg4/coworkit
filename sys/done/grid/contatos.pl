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
print ">C&oacute;digo</th>\n";

print "			<th id='contato' width=15% onClick=\"orderby('contato')\"";
if($ORDER eq "contato")
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
print ">Contato</th>\n";

print "			<th id='valor' onClick=\"orderby('valor')\"";
if($ORDER eq "valor")
	{
	print " class='asc'";
	}
elsif($ORDER eq "valor desc")
	{
	print " class='desc'";
	}
else
	{
	print " class='thor'";
	}
print ">Valor</th>\n";

print "			<th id='empresa' width=25% onClick=\"orderby('empresa')\"";
if($ORDER eq "empresa")
	{
	print " class='asc'";
	}
elsif($ORDER eq "empresa desc")
	{
	print " class='desc'";
	}
else
	{
	print " class='thor'";
	}
print ">Empresa</th>\n";

if($show_emp_apelido)
	{
	$qtdcmp++;
	print "			<th id='apelido' width=20% onClick=\"orderby('apelido')\"";
	if($ORDER eq "apelido")
		  {
		  print " class='asc'";
		  }
	elsif($ORDER eq "apelido desc")
		  {
		  print  " class='desc'";
		  }
	else
		  {
		  print " class='thor'";
		  }
	print  ">Apelido</th>\n";
	}


print<<END;
		</tr>
	</thead>
	<tbody>
END

# $SQL = "select * from contato_empresa_view where parceiro = $USER->{empresa}";

# Se for selecionado algum grupo, SQL2 faz um join na tabela de grupos
# if($GRUPO ne "")
#	{
#	$SQL .= " join empresa_relacionamento on empresa.codigo = empresa_relacionamento.empresa and empresa_relacionamento.relacionamento = '$GRUPO' ";
#	}

$SQL .= " where contato_dados.nome is not null and contato_dados.nome not like '' ";

if($CAMPO ne "" && ($PESQLETRA ne "" || $PESQ ne ""))
	{
	if($CAMPO eq "tipo")
		{
		$CAMPO = "tipo_contato.descrp";
		}
	elsif($CAMPO eq "empresa")
		{
		$CAMPO = "empresa.nome";
		}
	else
		{
		$CAMPO = "contato_dados.".$CAMPO;
		}
	if($CAMPO eq "contato_dados.codigo")
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
			$SQL .= " <=> '$PESQLETRA%' ";
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
		$SQL .= " and contato_dados.nome ~ '(^[0-9])' ";
		}
	elsif($PESQLETRA ne "")
		{
		$SQL .= " and (contato_dados.nome <=> '%$PESQLETRA%' or empresa.nome <=> '$PESQLETRA%' or empresa.apelido <=> '$PESQLETRA%') ";
		}
	elsif($PESQ ne "")
		{
		$SQL .= " and (contato_dados.nome <=> '%$PESQ%' or empresa.nome <=> '%$PESQ%' or empresa.apelido <=> '%$PESQ%') ";
		}
	}

if($ORDER eq "codigo")
	{
	$SQL .= "order by contato_dados.codigo";
	}
elsif($ORDER eq "codigo desc")
	{
	$SQL .= "order by contato_dados.codigo desc";
	}
elsif($ORDER eq "empresa")
	{
	$SQL .= "order by empresa.nome, descrp, tipo_contato.descrp, contato_dados.valor";
	}
elsif($ORDER eq "empresa desc")
	{
	$SQL .= "order by empresa.nome desc, descrp desc, tipo_contato.descrp desc, contato_dados.valor desc";
	}
elsif($ORDER eq "tipo")
	{
	$SQL .= "order by tipo_contato.descrp, contato_dados.valor";
	}
elsif($ORDER eq "tipo desc")
	{
	$SQL .= "order by tipo_contato.descrp desc, contato_dados.valor desc";
	}
elsif($ORDER eq "valor")
	{
	$SQL .= "order by contato_dados.valor, tipo_contato.descrp";
	}
elsif($ORDER eq "valor desc")
	{
	$SQL .= "order by contato_dados.valor desc, tipo_contato.descrp desc";
	}
elsif($ORDER eq "contato desc")
	{
	$SQL .= "order by descrp desc, tipo_contato.descrp desc, contato_dados.valor desc, empresa.nome desc ";
	}
else
	{
	$SQL .= "order by descrp, tipo_contato.descrp, contato_dados.valor, empresa.nome ";
	}
	
$SQL = "select * from contato_empresa_view where parceiro = $USER->{empresa}";
$sth = &DBE($SQL);
$rv = $sth->rows();
if($rv < 1)
	{
print<<END;
	<tr>
		<td colspan=5>Nenhum contato encontrado</td>
	</tr>
END
	}
else
	{
	while($contato = $sth->fetchrow_hashref)
		{
		$contato_dados = "";
		$DBD = &DBE("select cd.*, tc.descrp as tipo_contato from contato_dados as cd left join tipo_contato as tc on tc.codigo = cd.tipo where cd.contato_endereco = $contato->{codigo}");
		while($cdados = $DBD->fetchrow_hashref)
			{
			$contato_dados .= $cdados->{tipo_contato}.": ".$cdados->{valor}."<br> ";
			}
			
print<<END;
		<tr id='$contato->{'empresa'}' onDblClick='view("$contato->{'empresa'}")' onClick='pre_view("$contato->{'empresa'}")'>
			<td title='$contato->{'codigo'}'>$contato->{'codigo'}</td>
			<td title='$contato->{'descrp'}'>$contato->{'descrp'}</td>
			<td title='$contato_dados'>$contato_dados</td>
			<td title='$contato->{'nome'}'>$contato->{'nome'}</td>
END
if($show_emp_apelido)
	{
print<<END;
			<td title='$contato->{'apelido'}' $ns>$contato->{'apelido'}</td>
END
	}
print<<END;
		</tr>
END
		}
	}
print<<END;
	</tbody>
</table>
</div>
END
