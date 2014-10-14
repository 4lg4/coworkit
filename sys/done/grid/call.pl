use Tie::IxHash;
tie %cols, "Tie::IxHash";

if($ORDER eq "")
	{
	$ORDER = "dt_open";
	}

%cols = (
dtopen_formatada => 'Abertura',
call_codigo => 'Chamado',
status_dt => 'Alterado',
dtag => 'DTAG',
tipo_descrp => 'Tipo',
call_status => 'Status',
prioridade_descrp => 'Urgente',
call_descrp => 'Problema',
tecnico_nome => 'Tecnico',
empresa_nome => 'Cliente'
);


print<<END;
<div id="grid_scroll">
<table width=100% border=0 cellpadding=4 cellspacing=2 class="navigateable" id="grid_call" style="border: solid 1px #808080">
	<thead>
		<tr>
END
while(my ($key, $value) = each(%cols))
	{
	print "<th";
	print " id='$key' ";
	if($key eq "bloqueado")
		{
		print " width=5%";
		}
	elsif($key eq "dtcad")
		{
		print " width=10%";
		}
	elsif($key eq "nivel")
		{
		print " width=10%";
		}
	print " onClick=\"orderby('$key')\"";
	if($ORDER eq $key)
		{
		print " class='asc'";
		}
	elsif($ORDER eq $key." desc")
		{
		print " class='desc'";
		}
	else
		{
		print " class='thor'";
		}
	print ">".$value."</th>";
	}
print<<END;
		</tr>
	</thead>
	<tbody>
END

$SQL = "select *, to_char(dt_open, 'DD/MM/YYYY às HH24:MIh') as dtopen_formatada, to_char(status_dt, 'DD/MM/YYYY às HH24:MIh') as status_dt_formatada from call_lista_distinct ";
if($PESQLETRA ne "" || $PESQ ne "")
	{
	$SQL .= " where ";
	}
if($CAMPO ne "" && ($PESQLETRA ne "" || $PESQ ne ""))
	{
	if($CAMPO eq "call_codigo")
		{
		$SQL .= $CAMPO;
		$SQL .= "=";
		if($PESQ =~ /[a-zA-Z]/)
			{
			$SQL .= " '0' ";
			}
		else
			{
			$SQL .= " '$PESQ' ";
			}
		}
	else
		{
		$SQL .= $CAMPO;
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
	}
else
	{
	if($PESQLETRA ne "")
		{
		$SQL .= " call_codigo <=> '$PESQLETRA%' or call_descrp <=> '$PESQLETRA%' ";
		}
	elsif($PESQ ne "")
		{
		$SQL .= " call_codigo <=> '%$PESQ%' or call_descrp <=> '%$PESQ%' ";
		}
	}


if($ORDER eq "call_codigo")
	{
	$SQL .= "order by call_codigo";
	}
elsif($ORDER eq "call_codigo desc")
	{
	$SQL .= "order by call_codigo desc";
	}
elsif($ORDER eq "status_dt")
	{
	$SQL .= "order by status_dt, dt_open";
	}
elsif($ORDER eq "status_dt desc")
	{
	$SQL .= "order by status_dt desc, dt_open desc";
	}
elsif($ORDER eq "dtag")
	{
	$SQL .= "order by dtag NULLS FIRST, dt_open";
	}
elsif($ORDER eq "dtag desc")
	{
	$SQL .= "order by dtag desc NULLS LAST, dt_open desc";
	}
elsif($ORDER eq "tipo_descrp")
	{
	$SQL .= "order by tipo_descrp, dt_open";
	}
elsif($ORDER eq "tipo_descrp desc")
	{
	$SQL .= "order by tipo_descrp desc, dt_open desc";
	}
elsif($ORDER eq "call_status")
	{
	$SQL .= "order by call_status, dt_open";
	}
elsif($ORDER eq "call_status desc")
	{
	$SQL .= "order by call_status desc, dt_open desc";
	}
elsif($ORDER eq "prioridade_descrp")
	{
	$SQL .= "order by prioridade_descrp, dt_open";
	}
elsif($ORDER eq "prioridade_descrp desc")
	{
	$SQL .= "order by prioridade_descrp desc, dt_open desc";
	}
elsif($ORDER eq "call_descrp")
	{
	$SQL .= "order by call_descrp, dt_open";
	}
elsif($ORDER eq "call_descrp desc")
	{
	$SQL .= "order by call_descrp desc, dt_open desc";
	}
elsif($ORDER eq "usuario_nome")
	{
	$SQL .= "order by tecnico_nome NULLS FIRST, dt_open";
	}
elsif($ORDER eq "tecnico_nome desc")
	{
	$SQL .= "order by tecnico_nome desc NULLS LAST, dt_open desc";
	}
elsif($ORDER eq "empresa_nome")
	{
	$SQL .= "order by empresa_nome, dt_open";
	}
elsif($ORDER eq "empresa_nome desc")
	{
	$SQL .= "order by empresa_nome desc, dt_open desc";
	}
elsif($ORDER eq "dtopen_formatada desc")
	{
	$SQL .= "order by dt_open desc, call_codigo desc";
	}
else
	{
	$SQL .= "order by dt_open, call_codigo";
	}
$SQL .= ", status_dt desc";

$sth = &select($SQL);
$rv = $sth->rows();
if($rv < 1)
	{
print<<END;
	<tr>
		<td colspan=4>Nenhum chamado encontrado</td>
	</tr>
END
	}
else
	{
	while($row = $sth->fetchrow_hashref)
		{
		$tecnico = $row->{'tecnico_nome'};
		$tecnico_nome = $tecnico;
		if($tecnico ne "")
			{
			if($row->{'tecnico_nome'} ne "")
				{
				$tecnico = $row->{'tecnico_nome'}." (".$row->{'tecnico_codigo'}.")";
				$tecnico_nome = $row->{'tecnico_nome'};
				}
			}
		if($row->{'prioridade_codigo'} eq "2")
			{
			$urgente = "sim";
			}
		else
			{
			$urgente = "não";
			}
print<<END;
		<tr id='$row->{'call_codigo'}' onDblClick='view("$row->{'call_codigo'}")'>
			<td align=center width=120 title='$row->{'dtopen_formatada'}'>$row->{'dtopen_formatada'}</td>
			<td align=center width=100 title='$row->{'call_codigo'}'>
END
		printf "%07d", $row->{'call_codigo'};
print<<END;
			</td>
			<td align=center width=120 title='$row->{'status_dt_formatada'}'>$row->{'status_dt_formatada'}</td>
			<td width=100 title='$row->{'dtag'}'>$row->{'dtag'}</td>
			<td align=center width=100 title='$row->{'tipo_descrp'}'>$row->{'tipo_descrp'}</td>
			<td align=center width=100 title='$row->{'call_status'}'>$row->{'call_status'}</td>
			<td align=center width=50 title='$row->{'prioridade_descrp'}'>$urgente</td>
			<td title='$row->{'call_descrp'}'>$row->{'call_descrp'}</td>
			<td width=15% title='$tecnico'>$tecnico_nome</td>
			<td width=20% title='$row->{'empresa_nome'}'>$row->{'empresa_nome'}</td>
		</tr>
END
		}
	}
print<<END;
	</tbody>
</table>
</div>
END
