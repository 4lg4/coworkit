use Tie::IxHash;
tie %cols, "Tie::IxHash";

$EMPRESA = &get("EMPRESA"); # pega dado do select empresa do formulario em start.cgi

if($ORDER eq "")
	{
	$ORDER = "login";
	}

%cols = (
login => 'Usuário',
nome => 'Nome',
empresa => 'Empresa',
email => 'E-Mail',
tipo => 'Tipo de Usuário',
data => 'Data de Cadastro'
);


print<<END;
<div id="grid_scroll">
<table width=100% border=0 cellpadding=4 cellspacing=0 class="navigateable" id="grid">
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
	elsif($key eq "login")
		{
		print " width=15%";
		}
	elsif($key eq "data")
		{
		print " width=10%";
		}
	elsif($key eq "tipo")
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

$SQL = "select *, usuario.nome as usuario_nome, to_char(data, 'DD/MM/YYYY HH:MM') as data_formatada, usuario_tipo.descrp as usuario_tipo, empresa.nome as empresa_nome, usuario.img as usuario_img from usuario join usuario_tipo on usuario.tipo = usuario_tipo.codigo left join empresa on usuario.empresa = empresa.codigo ";
	
if($PESQLETRA ne "" || $PESQ ne "" || $EMPRESA ne "")
	{
	$SQL .= " where ";
	}

# Se for selecionado alguma empresa
if($EMPRESA ne "")
	{
	$SQL .= " usuario.empresa = '$EMPRESA' ";
	if($PESQLETRA ne "" || $PESQ ne "")
		{
		$SQL .= " and ";
		}
	}	
	
if($CAMPO ne "" && ($PESQLETRA ne "" || $PESQ ne ""))
	{
	$CAMPO = "usuario.".$CAMPO;
	if($CAMPO eq "usuario.usuario")
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
		$SQL .= " usuario.login <=> '$PESQLETRA%' or usuario.nome <=> '$PESQLETRA%' ";
		}
	elsif($PESQ ne "")
		{
		$SQL .= " usuario.login <=> '%$PESQ%' or usuario.nome <=> '%$PESQ%' ";
		}
	}

if($ORDER eq "bloqueado")
	{
	$SQL .= "order by usuario.bloqueado, usuario.login";
	}
elsif($ORDER eq "bloqueado desc")
	{
	$SQL .= "order by usuario.bloqueado desc, usuario.login";
	}
elsif($ORDER eq "empresa")
	{
	$SQL .= "order by empresa.nome, usuario.login";
	}
elsif($ORDER eq "empresa desc")
	{
	$SQL .= "order by empresa.nome desc, usuario.login desc";
	}
elsif($ORDER eq "tipo")
	{
	$SQL .= "order by usuario_tipo.descrp, usuario.login";
	}
elsif($ORDER eq "tipo desc")
	{
	$SQL .= "order by usuario_tipo.descrp desc, usuario.login desc";
	}
elsif($ORDER eq "data")
	{
	$SQL .= "order by usuario.data, usuario.login";
	}
elsif($ORDER eq "data desc")
	{
	$SQL .= "order by usuario.data desc, usuario.login desc";
	}
elsif($ORDER eq "email")
	{
	$SQL .= "order by usuario.email, usuario.login";
	}
elsif($ORDER eq "email desc")
	{
	$SQL .= "order by usuario.email desc, usuario.login desc";
	}
elsif($ORDER eq "nome")
	{
	$SQL .= "order by usuario.nome, usuario.login";
	}
elsif($ORDER eq "nome desc")
	{
	$SQL .= "order by usuario.nome desc, usuario.login desc";
	}
elsif($ORDER eq "login desc")
	{
	$SQL .= "order by usuario.login desc ";
	}
else
	{
	$SQL .= "order by usuario.login ";
	}
	
$sth = &select($SQL);
$rv = $sth->rows();
if($rv < 1)
	{
print<<END;
	<tr>
		<td colspan=4>Nenhum usuário encontrado</td>
	</tr>
END
	}
else
	{
	while($row = $sth->fetchrow_hashref)
		{
		
		if($row->{usuario_img} ne "")
			{
			$img_liberado = "<img src='/sys/cfg/DPAC/view_avatar.cgi?MD5=".$row->{usuario_img}."' border=0 alt='avatar' align='absmiddle' width=35 height=35 style='margin-right: 5px'>";
			}
		else
			{
			$img_liberado = "<img src='/img/usuario/default_man.png' border=0 alt='avatar_padrao' align='absmiddle' width=35 height=35 style='margin-right: 5px'>";
			}
		
print<<END;
		<tr id='$row->{'usuario'}' onDblClick='view("$row->{'usuario'}")' onClick='pre_view("$row->{'usuario'}")'>
			<td title='$row->{'login'}'>$img_liberado $row->{'login'}</td>
			<td title='$row->{'usuario_nome'}'>$row->{'usuario_nome'}</td>
			<td title='$row->{'empresa_nome'}'>$row->{'empresa_nome'}</td>
			<td title='$row->{'email'}'>$row->{'email'}</td>
			<td title='$row->{'usuario_tipo'}'>$row->{'usuario_tipo'}</td>
			<td align=center title='$row->{'data_formatada'}'>$row->{'data_formatada'}</td>
		</tr>
END
		}
	}
print<<END;
	</tbody>
</table>
</div>
END
