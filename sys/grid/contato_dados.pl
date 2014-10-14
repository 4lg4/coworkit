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
<table width=100% border=0 cellpadding=4 cellspacing=2 class="navigateable" id="grid">
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

print "			<th id='tipo' width=10% onClick=\"orderby('tipo')\"";
if($ORDER eq "tipo")
	{
	print " class='asc'";
	}
elsif($ORDER eq "tipo desc")
	{
	print " class='desc'";
	}
else
	{
	print " class='thor'";
	}
print ">Tipo</th>\n";

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

$SQL = "select *, empresa.codigo as cod_emp, empresa.nome as nome_emp, empresa.apelido as apelido_emp, endereco_contato.codigo as cod_contato, endereco_contato.nome as nome_contato, endereco_contato.valor as valor_contato, initcap(tipo_contato.descrp) as tipo_contato from endereco_contato join tipo_contato on endereco_contato.tipo = tipo_contato.codigo join empresa_endereco on endereco_contato.endereco = empresa_endereco.codigo join empresa on empresa_endereco.empresa = empresa.codigo ";

# Se for selecionado algum grupo, SQL2 faz um join na tabela de grupos
if($GRUPO ne "")
	{
	$SQL .= " join empresa_relacionamento on empresa.codigo = empresa_relacionamento.empresa and empresa_relacionamento.relacionamento = '$GRUPO' ";
	}

# Testa para ver se é parceiro
$sth4 = &select("select * from pg_tables where tablename='parceiro_empresa'");
$rv4 = $sth4->rows();
if($rv4 > 0)
	{
	# Se for parceiro, trás só os dados o parceiro
	$SQL .= " join parceiro_empresa on empresa.codigo = parceiro_empresa.empresa and parceiro_empresa.parceiro = '$LOGEMPRESA' ";
	}

$SQL .= " where endereco_contato.nome is not null and endereco_contato.nome not like '' ";

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
		$CAMPO = "endereco_contato.".$CAMPO;
		}
	if($CAMPO eq "endereco_contato.codigo")
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
		$SQL .= " and endereco_contato.nome ~ '(^[0-9])' ";
		}
	elsif($PESQLETRA ne "")
		{
		$SQL .= " and (endereco_contato.nome <=> '%$PESQLETRA%' or empresa.nome <=> '$PESQLETRA%' or empresa.apelido <=> '$PESQLETRA%') ";
		}
	elsif($PESQ ne "")
		{
		$SQL .= " and (endereco_contato.nome <=> '%$PESQ%' or empresa.nome <=> '%$PESQ%' or empresa.apelido <=> '%$PESQ%') ";
		}
	}

if($ORDER eq "codigo")
	{
	$SQL .= "order by endereco_contato.codigo";
	}
elsif($ORDER eq "codigo desc")
	{
	$SQL .= "order by endereco_contato.codigo desc";
	}
elsif($ORDER eq "empresa")
	{
	$SQL .= "order by empresa.nome, nome_contato, tipo_contato.descrp, endereco_contato.valor";
	}
elsif($ORDER eq "empresa desc")
	{
	$SQL .= "order by empresa.nome desc, nome_contato desc, tipo_contato.descrp desc, endereco_contato.valor desc";
	}
elsif($ORDER eq "tipo")
	{
	$SQL .= "order by tipo_contato.descrp, endereco_contato.valor";
	}
elsif($ORDER eq "tipo desc")
	{
	$SQL .= "order by tipo_contato.descrp desc, endereco_contato.valor desc";
	}
elsif($ORDER eq "valor")
	{
	$SQL .= "order by endereco_contato.valor, tipo_contato.descrp";
	}
elsif($ORDER eq "valor desc")
	{
	$SQL .= "order by endereco_contato.valor desc, tipo_contato.descrp desc";
	}
elsif($ORDER eq "contato desc")
	{
	$SQL .= "order by nome_contato desc, tipo_contato.descrp desc, endereco_contato.valor desc, empresa.nome desc ";
	}
else
	{
	$SQL .= "order by nome_contato, tipo_contato.descrp, endereco_contato.valor, empresa.nome ";
	}

$sth = &select($SQL);
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
	while($row = $sth->fetchrow_hashref)
		{
print<<END;
		<tr id='$row->{'cod_emp'}' onDblClick='view("$row->{'cod_emp'}")' onClick='pre_view("$row->{'cod_emp'}")'>
			<td title='$row->{'cod_contato'}'>$row->{'cod_contato'}</td>
			<td title='$row->{'nome_contato'}'>$row->{'nome_contato'}</td>
			<td title='$row->{'tipo_contato'}'>$row->{'tipo_contato'}</td>
			<td title='$row->{'valor_contato'}'>$row->{'valor_contato'}</td>
			<td title='$row->{'nome_emp'}'>$row->{'nome_emp'}</td>
END
if($show_emp_apelido)
	{
print<<END;
			<td title='$row->{'apelido_emp'}' $ns>$row->{'apelido_emp'}</td>
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
