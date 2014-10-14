
$PESQ = &get('PESQ');
$CAMPO = &get('CAMPO');
$ORDER = &get('ORDER');
$PESQLETRA = &get('PESQLETRA');
$ID = &get('ID');

# $SQL = "select *, upper(sem_acento(substring(emp_nome,1,1))) as letra_inicial from empresas_lista_distinct ";

# Testa para ver se é parceiro
#$sth4 = &select("select * from pg_tables where tablename='parceiro_empresa'");
#$rv4 = $sth4->rows();
#if($rv4 > 0)
#{
# se for parceiro acrescenta no SQL
	$SQL = " select *, upper(sem_acento(substring(emp_nome,1,1))) as letra_inicial from empresas_lista_distinct  join parceiro_empresa on empresas_lista_distinct.emp_codigo = parceiro_empresa.empresa and parceiro_empresa.parceiro = ".$USER->{empresa};
#}


# print $query->header({charset=>utf8});	
# debug($SQL);
# exit;

# $sth = &select($SQL);
# $rv = $sth->rows();

	
if($PESQLETRA ne "" || $PESQ ne "")
	{
	$SQL .= " where ";
	}
elsif($CODIGO ne "")
	{
	$SQL .= " where empresas_lista_distinct.emp_codigo = '$CODIGO' ";
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
		$SQL .= " empresas_lista_distinct.emp_nome <=> '%$PESQ%' ";
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
elsif($ORDER eq "tipo")
	{
	$SQL .= "order by emp_tipo_descr NULLS first";
	}
elsif($ORDER eq "tipo desc")
	{
	$SQL .= "order by emp_tipo_descr desc NULLS last";
	}
elsif($ORDER eq "endereco")
	{
	$SQL .= "order by end_endereco NULLS first";
	}
elsif($ORDER eq "endereco desc")
	{
	$SQL .= "order by end_endereco desc NULLS last";
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

# print $query->header({charset=>utf8});	
# debug($SQL);
# exit;

$sth = &DBE($SQL);
$rv = $sth->rows();

if($rv < 1)
	{
	print $query->header({charset=>utf8});
print<<END;
	<html><body style='margin-top: 40%'>
		<center>Nenhuma empresa encontrada</center>
	</body></html>
END
	exit;
	}
	
return true;
