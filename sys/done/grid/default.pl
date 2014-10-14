use POSIX qw(strtod setlocale LC_NUMERIC);
setlocale(LC_NUMERIC, "pt_BR.UTF-8");

if($SHOW eq "usuarios")
	{
	$TABLE = "usuario";
	}
else
	{
	$TABLE = $SHOW;
	}

# Encontra os campos da tabela
$SQL = "select column_name, data_type, character_maximum_length, is_nullable from information_schema.columns where table_name = '$TABLE' $SQL order by ordinal_position";

$sth = &select($SQL);
$rv = $sth->rows();
if($rv > 0)
	{
	$cols = $sth->fetchall_arrayref();
	}

print<<END;

<style>
.hidden_class {
    display:none;
}
</style>

<div id="grid_scroll">
<table width=100% border=0 cellpadding=4 cellspacing=0 class="navigateable" id="grid">
	<thead>
		<tr>
END
$TCOD = "char";
# Imprime o nome das colunas
foreach $row(@{$cols})
	{
        # campo parceiro já vem preenchido e escondido 
        $hidden  = "";
        if(lc(@$row[0]) eq "parceiro" || lc(@$row[0]) eq "pai" || lc(@$row[0]) eq "exportar" || lc(@$row[0]) eq "restrito" || lc(@$row[0]) eq "obrigatorio") { 
            $hidden = "hidden_class";
        }
        
        
	if($ORDER eq "")
		{
		if(@$row[0] eq "codigo")
			{
			$ORDER = "codigo";
			if(@$row[1] eq "bigint" || @$row[1] eq "integer")
				{
				$TCOD = "number";
				}
			}
		elsif(@$row[0] eq "cod")
			{
			$ORDER = "cod";
			if(@$row[1] eq "bigint" || @$row[1] eq "integer")
				{
				$TCOD = "number";
				}
			}
		}
	print "<th";
	print " id='@$row[0]' ";
	if($CAMPO eq @$row[0])
		{
		$TIPO = @$row[1];
		}
	if(@$row[1] eq "bigint" || @$row[1] eq "integer" || @$row[1] eq "numeric")
		{
		print " width=8%";
		}
	elsif(@$row[1] eq "character" && @$row[2] eq "1")
		{
		print " width=8%";
		}
	print " onClick=\"orderby('@$row[0]')\"";
	if($ORDER eq @$row[0])
		{
		print " class='asc'";
		}
	elsif($ORDER eq @$row[0]." desc")
		{
		print " class='desc'";
		}
	else
		{
		print " class='thor'";
		}
	print "><span class='$hidden'>".&traduz(@$row[0])."</span></th>";
	}
print<<END;
		</tr>
	</thead>
	<tbody>
END

# Verifica se tem chave estrangeira
foreach $row(@{$cols})
	{
	$VIEW = $TABLE;
	$VIEW =~ s/_lista$//;
	$sth2 = &select("SELECT ccu.table_name AS references_table, ccu.column_name AS references_field FROM information_schema.table_constraints tc LEFT JOIN information_schema.key_column_usage kcu ON tc.constraint_catalog = kcu.constraint_catalog AND tc.constraint_schema = kcu.constraint_schema AND tc.constraint_name = kcu.constraint_name LEFT JOIN information_schema.referential_constraints rc ON tc.constraint_catalog = rc.constraint_catalog AND tc.constraint_schema = rc.constraint_schema AND tc.constraint_name = rc.constraint_name LEFT JOIN information_schema.constraint_column_usage ccu ON rc.unique_constraint_catalog = ccu.constraint_catalog AND rc.unique_constraint_schema = ccu.constraint_schema AND rc.unique_constraint_name = ccu.constraint_name WHERE (tc.table_name = '$TABLE' or tc.table_name = '$VIEW') and tc.constraint_type ilike 'foreign key' and kcu.column_name = '@$row[0]'  ");

	$rv2 = $sth2->rows();
	if($rv2 > 0)
		{
		while($row2 = $sth2->fetch)
			{
			$fkeycol{@$row[0]} = @$row[0];
			$fkeytabref{@$row[0]} = @$row2[0];
			$fkeycolref{@$row[0]} = @$row2[1];

			# Identifica o nome da coluna de descrição da chave estrangeira
			$sth21 = &select("select column_name from information_schema.columns where table_name = '@$row2[0]' and column_name ilike 'descrp' or column_name ilike 'nome' order by column_name limit 1 ");
			$rv21 = $sth21->rows();
			if($rv21 > 0)
				{
				while($row21 = $sth21->fetch)
					{
					$fkeydescr{@$row[0]} = @$row21[0];
					}
				}
			else
				{
				$fkeydescr{@$row[0]} = @$row2[1];
				}
			$sth21->finish;
			}
		}
	else
		{
		$fkeycol{@$row[0]} = '';
		$fkeytabref{@$row[0]} = '';
		$fkeycolref{@$row[0]} = '';
		$fkeydescr{@$row[0]} = '';
		}
	}

# Monta o SQL que busca os dados da tabela de fato
$SQL = "select $TABLE.* from $TABLE ";

# Testa para ver se parceiro
$sth4 = &select("select * from pg_tables where tablename='parceiro_".$TABLE."'");
$rv4 = $sth4->rows();
if($rv4 > 0)
	{
	# Se for parceiro, trás só os dados o parceiro
	$SQL .= " join parceiro_".$TABLE." on ".$TABLE.".codigo = parceiro_".$TABLE.".$TABLE and parceiro_".$TABLE.".parceiro = '$LOGEMPRESA' ";
	}

if($TCOD eq "number")
	{
	if($ORDER eq "codigo")
		{
		$SQL .= " where ".$TABLE.".codigo > 0 ";
		}
	elsif($ORDER eq "cod")
		{
		$SQL .= " where ".$TABLE.".cod > 0 ";
		}
	if($PESQLETRA ne "" || $PESQ ne "")
		{
		$SQL .= " and ";
		}
	}
else
	{
	if($PESQLETRA ne "" || $PESQ ne "")
		{
		$SQL .= " where ";
		}
	}
if($CAMPO ne "" && ($PESQLETRA ne "" || $PESQ ne ""))
	{
	if($TIPO eq "integer" || $TIPO eq "bigint" || $TIPO eq "numeric")
		{
		$SQL .= $TABLE.".".$CAMPO;
		if($PESQLETRA ne "")
			{
			if($PESQLETRA eq "#")
				{
				$SQL .= " > 0 ";
				}
			elsif($PESQLETRA =~ /[a-zA-Z]/)
				{
				$SQL .= " = '0' ";
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
				if($PESQ ne "%")
					{
					$SQL .= " '$PESQ' ";
					}
				}
			}
		}
	elsif($TIPO ne "boolean")
		{
		$SQL .= $TABLE.".".$CAMPO;
		$SQL .= " <=> ";
		if($PESQLETRA ne "")
			{
			$SQL .= " '$PESQLETRA%' ";
			}
		elsif($PESQ ne "")
			{
			$SQL .= " '%$PESQ%' ";
			}
		}


	if($fkeytabref{$CAMPO} ne "")
		{
		if($SQL !~ /$TABLE.$fkeycol{$CAMPO} = $fkeytabref{$CAMPO}.$fkeycolref{$CAMPO}/)
			{
			$SQL =~ s/where/join $fkeytabref{$CAMPO} on $TABLE.$fkeycol{$CAMPO} = $fkeytabref{$CAMPO}.$fkeycolref{$CAMPO} where/;
			}
		$SQL .= " or ".$fkeytabref{$CAMPO}.".".$fkeydescr{$CAMPO}." <=> '";
		if($PESQLETRA ne "")
			{
			$SQL .= $PESQLETRA."%' ";
			}
		elsif($PESQ ne "")
			{
			$SQL .= "%".$PESQ."%' ";
			}
		}


	}
else
	{
	if($PESQLETRA ne "")
		{
		foreach $key(@{$cols})
			{
			if(@$key[1] eq "integer" or @$key[1] eq "bigint" or @$key[1] eq "numeric")
				{
				if($PESQLETRA eq "#")
					{
					$SQL .= " ".$TABLE.".".@$key[0]." ";
					$SQL .= " > 0 or ";
					}
				elsif($PESQLETRA =~ /[a-zA-Z]/)
					{
					# $SQL .= " = '0' or ";
					}
				else
					{
					$SQL .= " ".$TABLE.".".@$key[0]." ";
					$SQL .= " = '$PESQLETRA' or ";
					}
				}
			elsif(@$key[1] ne "boolean")
				{
				$SQL .= " ".$TABLE.".".@$key[0]." ";
				if($PESQLETRA eq "#")
					{
					$SQL .= " ~ '(^[0-9])' or ";
					}
				else
					{
					$SQL .= "<=> '$PESQLETRA%' or ";
					}
				}
			}
		}
	elsif($PESQ ne "")
		{
		foreach $key(@{$cols})
			{
			if(@$key[1] ne "boolean")
				{
				$SQL .= " ".$TABLE.".".@$key[0]." ";
				if(@$key[1] eq "integer" or @$key[1] eq "bigint" or @$key[1] eq "numeric")
					{
					if($PESQ =~ /[a-zA-Z]/)
						{
						$SQL .= " = '0' or ";
						}
					else
						{
						$SQL .= " = '$PESQ' or ";
						}
					}
				elsif(@$key[1] ne "boolean")
					{
					$SQL .= " <=> '%$PESQ%' or ";
					}
				}
			}
		}
	$SQL =~ s/ or $//;

	if($PESQLETRA ne "" || $PESQ ne "")
		{
		foreach $row(@{$cols})
			{
			if($fkeytabref{@$row[0]} ne "")
				{
				if($SQL !~ /$TABLE.$fkeycol{@$row[0]} = $fkeytabref{@$row[0]}.$fkeycolref{@$row[0]}/)
					{
					$SQL =~ s/where/join $fkeytabref{@$row[0]} on $TABLE.$fkeycol{@$row[0]} = $fkeytabref{@$row[0]}.$fkeycolref{@$row[0]} where/;
					}
				$SQL .= " or ".$fkeytabref{@$row[0]}.".".$fkeydescr{@$row[0]}." <=> '";
				if($PESQLETRA ne "")
					{
					$SQL .= $PESQLETRA."%' ";
					}
				elsif($PESQ ne "")
					{
					$SQL .= "%".$PESQ."%' ";
					}
				}
			}
		}
	}


# ajuste para core v3 (tabelas parceiro removidas)
if($TABLE eq "tipo_endereco" || $TABLE eq "tipo_doc" || $TABLE eq "tipo_contato") {
    $SQL .= "and ".$TABLE.".parceiro = ".$USER->{empresa};
}

# Verifica se tem ordenação
if($ORDER ne "")
	{
	# Encontra o campo na variável de ordenação
	$CMP = $ORDER;
	$CMP =~ s/ desc//;
	# Verifica se a ordenação é de alguma tabela estrangeira
	if($fkeytabref{$CMP} ne "")
		{
		# Verifica se no SQL não tem referência a tabela estrangeira (um join) e cria se for o caso
		if($SQL !~ /$fkeytabref{$CMP}/)
			{
			if($SQL =~ / join /)
				{
				$SQL =~ s/join/join $fkeytabref{$CMP} on $TABLE.$fkeycol{$CMP} = $fkeytabref{$CMP}.$fkeycolref{$CMP}/;
				}
			else
				{
				$SQL =~ s/from $TABLE/from $TABLE join $fkeytabref{$CMP} on $TABLE.$fkeycol{$CMP} = $fkeytabref{$CMP}.$fkeycolref{$CMP}/;
				}
			}
		$SQL .= " order by ".$fkeytabref{$CMP}.".".$fkeydescr{$CMP};
		if($ORDER =~ / desc/)
			{
			$SQL .= " desc";
			}
		}
	else
		{
		$SQL .= " order by ".$TABLE.".".$ORDER;
		}
	}
    
#debug($SQL);
$sth = &select($SQL);
$rv = $sth->rows();
if($rv < 1)
	{
print<<END;
	<tr>
		<td colspan=4>Nenhum registro encontrado</td>
	</tr>
<script language='JavaScript'>
	function view(x)
		{
		DActionAdd();
		}
</script>
END
	}
else
	{
	while($row = $sth->fetchrow_hashref)
		{
		print "<tr id='$row->{'codigo'}' onDblClick='view(\"$row->{'codigo'}\")' onClick='pre_view(\"$row->{'codigo'}\")'>";
		foreach $key(@{$cols})
			{ 
            
                # campo parceiro já vem preenchido e escondido 
                $hidden  = "";
                if(lc(@$key[0]) eq "parceiro" || lc(@$key[0]) eq "pai" || lc(@$key[0]) eq "exportar" || lc(@$key[0]) eq "restrito" || lc(@$key[0]) eq "obrigatorio") { 
                    $hidden = "hidden_class";
                }
                    
            
			print "<td title='@$key[0]' ";
			if(@$key[1] eq "numeric")
				{
				print " style='text-align: right; padding-right: 1%;'";
				}
			if(@$key[1] eq "boolean")
				{
				print " style='width: 8%; text-align: center; 1%;'";
				}
			print "> <span class='$hidden'>";
			if($fkeytabref{@$key[0]} ne "")
				{
				$sth3 = $dbh->prepare("select $fkeydescr{@$key[0]} from $fkeytabref{@$key[0]} where $fkeycolref{@$key[0]} = '$row->{@$key[0]}' ");
				$sth3->execute();
				$rv3 = $sth3->rows();
				if($rv3 > 0)
					{
					while($row3 = $sth3->fetch)
						{
						print "@$row3[0]";
						}
					}
				$sth3->finish;
				}
			else
				{
				if(@$key[1] eq "numeric")
					{
					printf("%.2f", $row->{@$key[0]});
					}
				elsif(@$key[1] eq "boolean")
					{
					if($row->{@$key[0]} eq "1")
						{
						print "<input type='checkbox' checked disabled>";
						}
					elsif($row->{@$key[0]} eq "0")
						{
						print "<input type='checkbox' disabled>";
						}
					}
				else
					{
					if(@$key[0] eq "cep")
						{
						print "<nobr>$row->{@$key[0]}</nobr>";
						}
					elsif(@$key[0] eq "timestamp")
						{
						print dateToShow($row->{@$key[0]});
						}
					else
						{
						if(@$key[1] eq "timestamp without time zone")
							{
							print dateToShow($row->{@$key[0]});
							}
						else
							{
							print "$row->{@$key[0]}";
							}
						}
					}
				}
			print "</span></td>";
			}
		print "</tr>";
		}
	}
print<<END;
	</tbody>
</table>
</div>
END
