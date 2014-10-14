$GRUPO = &get("GRUPO"); # pega dado do select grupos relacionados do formulario em start.cgi
$qtdcmp = 4;

$cfg_2 = &get_cfg(2);
if(&get_cfg(2) eq "")
	{
	$cfg_2 = "10"; # se vazio define numero minimo de linhas que sao mostradas
	}

if($ORDER eq "")
	{
	$ORDER = ""; # se vazio define qual campo sera a chave da ordenacao
	}
print<<END;
<!-- Bug no grid quando seleciona-se a letra D -->
<span><font color='#e5e5e5'> . </font></span>
<font color="#31517a"><b>Listagem que será impressa / exportada:</b></font><br>
<div id="grid_scroll" style="clear: both;">
<table width=100% border=0 cellpadding=4 cellspacing=2 class="navigateable" id="grid">
	<thead><tr>
END

$out = "<th id='codigo' width=5% onClick=\"orderby('codigo')\"";
if($ORDER eq "codigo")
	{
	$out .= " class='asc'";
	}
elsif($ORDER eq "codigo desc")
	{
	$out .= " class='desc'";
	}
else
	{
	$out .=  " class='thor'";
	}
$out .=  ">C&oacute;digo</th>\n";

$out .=  "			<th id='empresa' onClick=\"orderby('empresa')\"";
if($ORDER eq "empresa")
	{
	$out .=  " class='asc'";
	}
elsif($ORDER eq "empresa desc")
	{
	$out .=  " class='desc'";
	}
else
	{
	$out .=  " class='thor'";
	}
$out .=  ">Nome</th>\n";

if($show_emp_apelido)
	{
	$qtdcmp++;
	$out .=  "			<th id='endereco' width=25% onClick=\"orderby('endereco')\"";
	if($ORDER eq "endereco")
		  {
		  $out .=  " class='asc'";
		  }
	elsif($ORDER eq "end_endereco desc")
		  {
		  $out .=  " class='desc'";
		  }
	else
		  {
		  $out .=  " class='thor'";
		  }
	$out .=  ">Endereço</th>\n";
	}

$out .=  "			<th id='fone' width=15% onClick=\"orderby('fone')\"";
if($ORDER eq "fone")
	{
	$out .=  " class='asc'";
	}
elsif($ORDER eq "fone desc")
	{
	$out .=  " class='desc'";
	}
else
	{
	$out .=  " class='thor'";
	}
$out .=  ">Telefone</th>\n";

$out .=  "			<th id='email' width=25% onClick=\"orderby('email')\"";
if($ORDER eq "email")
	{
	$out .=  " class='asc'";
	}
elsif($ORDER eq "email desc")
	{
	$out .=  " class='desc'";
	}
else
	{
	$out .=  " class='thor'";
	}
$out .=  ">E-Mail</th>\n";
print $out;
print<<END;

		</tr>
	</thead>
	<tbody>
END

$SQL = "";


# SQL2 traz os dados da empresa
$SQL2 = "select * from empresas_lista_distinct  ";

# Se for selecionado algum grupo, SQL2 faz um join na tabela de grupos
if($GRUPO ne "")
	{
	$SQL2 .= " join empresa_relacionamento on empresas_lista_distinct.emp_codigo = empresa_relacionamento.empresa and empresa_relacionamento.relacionamento = '$GRUPO' ";
	}

# Testa para ver se é parceiro
$sth4 = &select("select * from pg_tables where tablename='parceiro_empresa'");
$rv4 = $sth4->rows();
if($rv4 > 0)
	{

	$SQL2 .= " join parceiro_empresa on empresas_lista_distinct.emp_codigo = parceiro_empresa.empresa and parceiro_empresa.parceiro = '$LOGEMPRESA' ";
	}

	






if($PESQLETRA ne "" || $PESQ ne "")
	{
	$SQL .= " where ";
	}
if($CAMPO ne "" && ($PESQLETRA ne "" || $PESQ ne ""))
	{
	if($CAMPO eq "codigo")
		{
		$SQL .= "empresas_lista_distinct.".$CAMPO;
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
			if($PESQ =~ /[a-zA-Z]/)
				{
				$SQL .= " = '0' ";
				}
			else
				{
				$SQL .= " = '$PESQ' ";
				}
			}
		}
	elsif($CAMPO eq "empresa_endereco.endereco")
		{
		$SQL =~ s/where/join empresa_endereco on empresas_lista_distinct.emp_codigo = empresa_endereco.empresa where/;
		$SQL .= $CAMPO;
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
	elsif($CAMPO =~ /^endereco_contato/)
		{
		$SQL =~ s/where/join empresa_endereco on empresas_lista_distinct.emp_codigo = empresa_endereco.empresa join endereco_contato on empresa_endereco.codigo = endereco_contato.endereco where/;
		
		if($CAMPO =~ /email/)
			{
			$SQL .= "endereco_contato.tipo = 4 and endereco_contato.valor ";
			}
		elsif($CAMPO =~ /fone/)
			{
			$SQL .= "endereco_contato.tipo = 1 and endereco_contato.valor ";
			}
		else
			{
			$SQL .= $CAMPO;
			}
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
	else
		{
		$SQL .= "empresas_lista_distinct.".$CAMPO;
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
		$SQL .= " empresas_lista_distinct.emp_nome ~ '(^[0-9])' ";
		}
	elsif($PESQLETRA ne "")
		{
		$SQL .= " empresas_lista_distinct.emp_nome <=> '$PESQLETRA%' ";
		}
	elsif($PESQ ne "")
		{
		$SQL .= " empresas_lista_distinct.emp_nome <=> '%$PESQ%' or empresas_lista_distinct.end_endereco <=> '%$PESQ%' ";
		}
	}

if($ORDER eq "codigo")
	{
	$SQL .= "order by emp_codigo";
	}
elsif($ORDER eq "codigo desc")
	{
	$SQL .= "order by emp_codigo desc";
	}
elsif($ORDER eq "fone")
	{
	$SQL .= "order by end_fone NULLS first";
	}
elsif($ORDER eq "fone desc")
	{
	$SQL .= "order by end_fone desc NULLS last";
	}
elsif($ORDER eq "email")
	{
	$SQL .= "order by end_mail NULLS first";
	}
elsif($ORDER eq "email desc")
	{
	$SQL .= "order by end_mail desc NULLS last";
	}
elsif($ORDER eq "endereco")
	{
	$SQL .= "order by end_endereco NULLS first, emp_nome";
	}
elsif($ORDER eq "endereco desc")
	{
	$SQL .= "order by end_endereco desc NULLS last, emp_nome desc";
	}
elsif($ORDER eq "empresa desc")
	{
	$SQL .= "order by emp_nome desc";
	}
else
	{
	$SQL .= "order by emp_nome";
	}
$SQL2 .= $SQL;
$sth = &select($SQL2);
$rv = $sth->rows();
@list_emails = "";
if(($SQL =~ /where/ || $GRUPO ne "") and $rv > 0)
	{
	while($row = $sth->fetchrow_hashref)
		{
		if($pwd =~ /syscall/)
			{
			if($row->{'end_mail'} ne "")
				{
				push @list_emails, $row->{'end_mail'};
				}
			}
		}
	if($rv <= $MAX)
		{
		$sth->finish;
		$sth = &select($SQL2);
		$rv = $sth->rows();
		}
	}
$NREG = $rv;
	
if($INI > 0)
	{
	$SQL2 .= " limit $MAX offset $INI";
	$sth = &select($SQL2);
	$rv = $sth->rows();
	}
elsif($rv > $MAX)
	{
	$SQL2 .= " limit $MAX";
	$sth = &select($SQL2);
	$rv = $sth->rows();
	}


if($rv < 1)
	{
print<<END;
	<tr>
		<td colspan=$qtdcmp>Nenhuma empresa encontrada</td>
	</tr>
END
	}
else
	{
	$n=0;
	$ns="";




	while($row = $sth->fetchrow_hashref)
		{
		$remail_emp = $row->{'end_mail'};
		$email_emp = "<a href='mailto:$row->{'end_mail'}'>".$row->{'end_mail'},"</a>";
print<<END;
		<tr onclick='on_prev($row->{emp_codigo})' onDblClick='view("$row->{'emp_codigo'}")'>
			<td title='$row->{'emp_codigo'}'>$row->{'emp_codigo'}</td>
			<td title='$row->{'emp_nome'}'>$row->{'emp_nome'}</td>
END
if($show_emp_apelido)
	{
print<<END;
			<td title='$row->{'end_endereco'}' $ns>$row->{'end_endereco'}</td>
END
	}
print<<END;

			<td title='$row->{'end_fone'}'>$row->{'end_fone'}</td>
			<td title='$remail_emp'>$email_emp</td>
		</tr>
END
		}
	}
print<<END;
	</tbody>
</table>
</div>
END

