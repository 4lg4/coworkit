$GRUPO = &get("GRUPO"); # pega dado do select grupos relacionados do formulario em start.cgi

$cfg_2 = &get_cfg(2);
if(&get_cfg(2) eq "")
	{
	$cfg_2 = "10"; # se vazio define numero minimo de linhas que sao mostradas
	}

if($ORDER eq "")
	{
	$ORDER = "empresa"; # se vazio define qual campo sera a chave da ordenacao
	}
print<<END;
<div id="grid_scroll" style="clear: both">
<table width=100% border=0 cellpadding=4 cellspacing=2 class="navigateable" id="grid">
	<thead>
		<tr>
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

$out .=  "			<th id='empresa' width=45% onClick=\"orderby('empresa')\"";
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

$out .=  "			<th id='fone' width=20% onClick=\"orderby('fone')\"";
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

$out .=  "			<th id='email' width=30% onClick=\"orderby('email')\"";
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
# SQL1 traz as últimas empresas visitadas
$SQL1 = "select *, last_view.dt as lastdt from empresas_lista_distinct left join last_view on (empresas_lista_distinct.emp_codigo = last_view.codigo and last_view.tabela = 'empresa' and last_view.usuario = '$LOGUSUARIO') ";

# SQL2 traz os dados da empresa
$SQL2 = "select * from empresas_lista_distinct ";

# Se for selecionado algum grupo, SQL2 faz um join na tabela de grupos
if($GRUPO ne "")
	{
	$SQL2 .= " join empresa_relacionamento on empresas_lista_distinct.emp_codigo = empresa_relacionamento.empresa and empresa_relacionamento.relacionamento = '$GRUPO' ";
	}


if($INI == 0 && $PESQLETRA eq "" && $PESQ eq "" && $GRUPO eq "")
	{
	$SQL1 .= $SQL;

	if($ORDER eq "codigo")
		{
		$SQL1 .= "order by last_view.dt desc NULLS last, emp_codigo";
		}
	elsif($ORDER eq "codigo desc")
		{
		$SQL1 .= "order by last_view.dt desc NULLS last, emp_codigo desc";
		}
	elsif($ORDER eq "fone")
		{
		$SQL1 .= "order by last_view.dt desc NULLS last, end_fone NULLS first";
		}
	elsif($ORDER eq "fone desc")
		{
		$SQL1 .= "order by last_view.dt desc NULLS last, end_fone desc NULLS last";
		}
	elsif($ORDER eq "email")
		{
		$SQL1 .= "order by last_view.dt desc NULLS last, end_mail NULLS first";
		}
	elsif($ORDER eq "email desc")
		{
		$SQL1 .= "order by last_view.dt desc NULLS last, end_mail desc NULLS last";
		}
	elsif($ORDER eq "empresa desc")
		{
		$SQL1 .= "order by last_view.dt desc NULLS last, emp_nome desc";
		}
	else
		{
		$SQL1 .= "order by last_view.dt desc NULLS last, emp_nome";
		}

	$SQL1 .= " limit $cfg_2";
	$sth2 = &select($SQL1);
	$rv2 = $sth2->rows();
	if($rv2 > 0)
		{
		$n=0;
		$ns="";
		while($row2 = $sth2->fetchrow_hashref)
			{
			$remail_emp = $row2->{'end_mail'};
			$email_emp = "<a href='mailto:$row2->{'end_mail'}'>".$row2->{'end_mail'},"</a>";
			if($n==0)
				{
				if($row2->{'lastdt'} ne "")
					{
					print "<tr id='$row2->{'emp_codigo'}'><td colspan=4 class='agrupo'>Últimas acessadas</td></tr>";
					$n++;
					}
				else
					{
					$n+=2;
					}
				}
			if($n==1)
				{
				if($ns eq "" || $ns eq "class='tdgrupo2'")
					{
					$ns = "class='tdgrupo1'";
					}
				else
					{
					$ns = "class='tdgrupo2'";
					}
				}
			else
				{
				$ns = "";
				}
print<<END;
		<tr id='$row2->{'emp_codigo'}' onDblClick='view("$row2->{'emp_codigo'}")' onClick='pre_view("$row2->{'emp_codigo'}")'>
			<td title='$row2->{'emp_codigo'}' $ns>$row2->{'emp_codigo'}</td>
			<td title='$row2->{'emp_nome'}' $ns>$row2->{'emp_nome'}</td>
			<td title='$row2->{'end_fone'}' $ns>$row2->{'end_fone'}</td>
			<td title='$remail_emp' $ns>$email_emp</td>
		</tr>
END
			}
		print "<tr id='$row2->{'emp_codigo'}'><td colspan=4 class='agrupo'>Outras</td></tr>\n";
		}
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
		$SQL .= " empresas_lista_distinct.emp_nome <=> '%$PESQ%' or empresas_lista_distinct.emp_apelido <=> '%$PESQ%' ";
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
		if($row->{'end_mail'} ne "")
			{
			push @list_emails, $row->{'end_mail'};
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
		<td colspan=4>Nenhuma empresa encontrada</td>
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
		<tr id='$row->{'emp_codigo'}' onDblClick='view("$row->{'emp_codigo'}")' onClick='pre_view("$row->{'emp_codigo'}")'>
			<td title='$row->{'emp_codigo'}'>$row->{'emp_codigo'}</td>
			<td title='$row->{'emp_nome'}'>$row->{'emp_nome'}</td>
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

$emails_bcc = join( ",", @list_emails);
$emails_bcc =~ s/^,//;
$emails_cep = $emails_bcc;
$emails_cep =~ s/,/,\\n/gm;
$emails_cep = "<div style='position: relative; left: -10px'>Não foi possível transferir a lista para seu programa de e-mails. Por favor, selecione, copie e cole manualmente.<br><br><textarea style='width: 350px; height: 260px;' onClick='this.select()'>".$emails_cep."</textarea></div>";

print "<script language='JavaScript'>";
if($emails_bcc ne "")
	{
	print "	show('icon_email');";
	}
else
	{
	print "	hide('icon_email');";
	}
print<<END;

	document.getElementById('foot').innerHTML='<form name="sendmail" method="post" action="mailto:?subject=$nome_emp&bcc=$emails_bcc" enctype="text/plain"></form>\\n';

	function sendmail()
		{
		try
			{
			document.sendmail.submit();
			}
		catch(err)
			{
			top.abre(top.document.title, "$emails_cep", 550, 320);
			}
		}
</script>
END


