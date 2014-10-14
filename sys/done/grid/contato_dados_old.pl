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

$SQL = "select * from contatos_list_view ";

# Se for selecionado algum grupo, SQL2 faz um join na tabela de grupos
if($GRUPO ne "")
	{
 	$SQL .= " join empresa_relacionamento on empresa_cod = empresa_relacionamento.empresa and empresa_relacionamento.relacionamento = '$GRUPO' ";
	}

# Testa para ver se é parceiro
$sth4 = &select("select * from pg_tables where tablename='parceiro_empresa'");
$rv4 = $sth4->rows();
if($rv4 > 0)
	{
	# Se for parceiro, trás só os dados o parceiro
  	$SQL .= " join parceiro_empresa on parceiro_empresa.empresa = empresa_cod and parceiro_empresa.parceiro = '$LOGEMPRESA' ";
	}

$SQL .= " where valor is not null and valor not like '' ";

if($CAMPO ne "" && ($PESQLETRA ne "" || $PESQ ne ""))
	{
	if($CAMPO eq "tipo")
		{
		$CAMPO = "tipo_descrp";
		}
	elsif($CAMPO eq "empresa")
		{
		$CAMPO = "empresa_contato";
		}
	else
		{
		$CAMPO = $CAMPO;
		}
	if($CAMPO eq "contato_cod")
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
		$SQL .= " and descricao ~ '(^[0-9])' ";
		}
	elsif($PESQLETRA ne "")
		{
		$SQL .= " and (descricao <=> '%$PESQLETRA%' or empresa_contato <=> '$PESQLETRA%' or apelido <=> '$PESQLETRA%') ";
		}
	elsif($PESQ ne "")
		{
		$SQL .= " and (descricao <=> '%$PESQ%' or empresa_contato <=> '%$PESQ%' or apelido <=> '%$PESQ%') ";
		}
	}

if($ORDER eq "codigo")
	{
	$SQL .= "order by contato_cod";
	}
elsif($ORDER eq "codigo desc")
	{
	$SQL .= "order by contato_cod desc";
	}
elsif($ORDER eq "empresa")
	{
	$SQL .= "order by empresa, descricao, tipo_descrp, valor";
	}
elsif($ORDER eq "empresa desc")
	{
	$SQL .= "order by empresa desc, descricao desc, tipo_descrp desc, valor desc";
	}
elsif($ORDER eq "tipo")
	{
	$SQL .= "order by tipo_descrp, valor";
	}
elsif($ORDER eq "tipo desc")
	{
	$SQL .= "order by tipo_descrp desc, valor desc";
	}
elsif($ORDER eq "valor")
	{
	$SQL .= "order by valor, tipo_descrp";
	}
elsif($ORDER eq "valor desc")
	{
	$SQL .= "order by valor desc, tipo_descrp desc";
	}
elsif($ORDER eq "contato desc")
	{
	$SQL .= "order by descricao desc, tipo_descrp desc, valor desc, empresa_contato desc ";
	}
else
	{
	$SQL .= "order by descricao, tipo_descrp, valor, empresa_contato ";
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
		<tr id='$row->{'empresa_cod'}' onDblClick='view("$row->{'empresa_cod'}")' onClick='pre_view("$row->{'empresa_cod'}")'>
			<td title='$row->{'contato_cod'}'>$row->{'contato_cod'}</td>
			<td title='$row->{'descricao'}'>$row->{'descricao'}</td>
			<td title='$row->{'tipo_descrp'}'>$row->{'tipo_descrp'}</td>
			<td title='$row->{'valor'}'>$row->{'valor'}</td>
			<td title='$row->{'empresa_contato'}'>$row->{'empresa_contato'}</td>
END
if($show_emp_apelido)
	{
print<<END;
			<td title='$row->{'apelido'}' $ns>$row->{'apelido'}</td>
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
