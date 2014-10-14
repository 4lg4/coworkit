#!/usr/bin/perl

$nacess = '204';
require "../cfg/init.pl";

$ID       = &get('ID');
$empresa  = &get('empresa');
$endereco = &get('endereco');
$grupo    = &get('grupo');
$agrupo   = &get('agrupo');


$GRUPO = $grupo;
$ENDERECO = $endereco;
$COD = $empresa;

# Busca o nome dos campos
$DB = DBE("
    select 
        *, 
        tipo_grupo_item.supervisor as hidden 
    from 
        grupo_item 
    join 
        tipo_grupo_item on grupo_item.tipo = tipo_grupo_item.codigo  
    where 
        grupo_item.grupo = $grupo 
    and tipo_grupo_item.descrp not ilike 'dtag'
    order by 
        seq
    limit 8
");

# cria matriz com o cabeçalho da tabela
$ncol = 0;

# No caso de ser multi empresa (busca ser apenas pelo grupo)
if(!$empresa)
	{
	$titulo_cod[$ncol]  = '';
	$titulo_desc[$ncol] = 'Empresa';
	$titulo_tam[$ncol] = 3;
	$tcol+=3;
	$ncol++;
	}
	
while($row = $DB->fetchrow_hashref)
	{
	$titulo_cod[$ncol]  = $row->{'codigo'};
	$titulo_desc[$ncol] = $row->{'descrp'};
	if(lc($titulo_desc[$ncol]) eq 'descrição')
		{
		# Campo grande, 4x
		$titulo_tam[$ncol] = 4;
		$tcol+=4;
		}
	elsif(lc($titulo_desc[$ncol]) eq 'porta' || lc($titulo_desc[$ncol]) eq 'tipo' || lc($titulo_desc[$ncol]) eq 'senha')
		{
		# Campo muito pequeno, 1x
		$titulo_tam[$ncol] = 1;
		$tcol+=1;
		}
	elsif(lc($titulo_desc[$ncol]) eq 'usuário' || lc($titulo_desc[$ncol]) eq 'ip interno' || lc($titulo_desc[$ncol]) eq 'servidor')
		{
		# Campo pequeno, 2x
		$titulo_tam[$ncol] = 2;
		$tcol+=2;
		}		
	else
		{
		# Campo normal, 3x
		$titulo_tam[$ncol] = 3;
		$tcol+=3;
		}		
	$ncol++;
	}
	
#
#   Dados TI
#       

# gera as "linhas" da tabela
$SQL = "select distinct ge.linha, ge.empresa, ge.endereco, e.apelido as empresa_nome, e.nome as empresa_razao from grupo_empresa as ge ";
$SQL .= "left join empresa as e on e.codigo = ge.empresa ";
$SQL .= "where ";
if($COD)
	{
	$SQL .= "ge.empresa = '$COD' and ";
	}
if($ENDERECO)
	{
	$SQL .= "ge.endereco = '$ENDERECO' and ";
	}
$SQL .= " ge.linha is not null and ";
$SQL .= "ge.grupo = '$GRUPO' ";
$DBI = DBE($SQL);
if($DBI->rows() > 0)
	{
	$nlin = 0;
	while($row2 = $DBI->fetchrow_hashref)
		{
		$COD = $row2->{'empresa'};
		$ENDERECO = $row2->{'endereco'};
		
		$linha_cod[$nlin] = $row2->{'linha'};

		for($e=0; $e<$ncol; $e++)
			{
			# gera cada coluna das linhas
			if($titulo_cod[$e] ne "")
				{
				$SQL = "select * from grupo_empresa where grupo_item = '$titulo_cod[$e]' and linha = '".$row2->{'linha'}."' and grupo_empresa.grupo = '$GRUPO' ";
				if($COD > 0)
					{
					$SQL .= "and grupo_empresa.empresa = '$COD' ";
					}
				  if($ENDERECO > 0)
					{
					$SQL .= "and grupo_empresa.endereco = '$ENDERECO' ";
					}
				$SQL .= "limit 1 ";

				$DBII = DBE($SQL);
				if($DBII->rows() == 0)
					{
					$linha_desc[$nlin][$e] = "&nbsp;";
					}
				else
					{
					while($row3 = $DBII->fetchrow_hashref)
						{
						$linha_desc[$nlin][$e] = $row3->{'valor'};
						&mnt_hide;
						}
					}
				}
			else
				{
				# mostra empresa se multi empresa (pesquisa apenas pelo grupo)
				if(!$empresa)
					{
					if($row2->{'empresa_nome'} =~ /[a-zA-Z]/)
						{
						$linha_desc[$nlin][$e] = $row2->{'empresa_nome'};
						}
					else
						{
						$linha_desc[$nlin][$e] = $row2->{'empresa_razao'};
						}
					&mnt_hide;
					}
				}
			}
		$nlin++;
		}
	}


# encontra um fator de multiplicação
$ref = 100 / $tcol;	
for($f=0; $f<$tcol; $f++)
	{
	$titulo_tam[$f] *= $ref;
	}

# Cria de fato o HTML
$R  = '{';
$R .= '    "title" :  "<div class=\"DTouchRadio_list_title\">';
for($f=0; $f<$ncol; $f++)
	{
	$R .= '<div style=\"text-align: left; width: '.$titulo_tam[$f].'%;\">'.$titulo_desc[$f].'</div>';
	}
$R .= '</div>", ';
$R .= '    "itens" : [';
for($f=0; $f<$nlin; $f++)
	{
	$R .= '{ "value" : ';
	$R .= $linha_cod[$f];
	$R .= ', "descrp": "<div class=\"DTouchRadio_list_line\" style=\"margin-left: -1% !important;\">';
	for($g=0; $g<$ncol; $g++)
		{
		$R .= '<div style=\"width: '.$titulo_tam[$g].'%;\" title=\"'.$linha_desc[$f][$g].'\">';
		if($linha_hide[$f][$g] ne "")
			{
			$R .= $linha_hide[$f][$g]
			}
		$R .= $linha_desc[$f][$g].'</div>';
		}
	$R .= '</div>"},';
	}
$R =~ s/,$//;
$R .= ']}';

print $query->header({charset=>utf8});
print $R;










sub mnt_hide
	{
	# Tipo, se for campo
	if(lc($titulo_desc[$e]) eq "tipo")
		{ 
		if(lc($linha_desc[$nlin][$e]) =~ m/ssh/)
			{
			$linha_hide[$nlin][$e] .= "<input type='hidden' name='tipo' value='ssh'>";
			}
		elsif(lc($linha_desc[$nlin][$e]) =~ m/rdp|ts/)
			{
			$linha_hide[$nlin][$e] = "<input type='hidden' name='tipo' value='rdp'>";
			}
		else
			{
			$linha_hide[$nlin][$e] = "<input type='hidden' name='tipo' value='".lc($linha_desc[$nlin][$e])."'>";
			}                            
		}
	elsif(lc($titulo_desc[$e]) eq "endereço externo")
		{ 
		$linha_hide[$nlin][$e] = "<input type='hidden' name='externo' value='".lc($linha_desc[$nlin][$e])."'>";
		}
	elsif(lc($titulo_desc[$e]) eq "empresa")
		{
		$linha_hide[$nlin][$e] = '<input type=\"hidden\" name=\"empresa\" value=\"'.$row2->{'empresa'}.'\">';
		$linha_hide[$nlin][$e] .= '<input type=\"hidden\" name=\"endereco\" value=\"'.$row2->{'endereco'}.'\">';	
		}
	elsif(lc($titulo_desc[$e]) eq "usuário")
		{ 
		$linha_hide[$nlin][$e] = "<input type='hidden' name='login' value='".$linha_desc[$nlin][$e]."'>";
		}
	elsif(lc($titulo_desc[$e]) eq "senha")
		{ 
		$linha_hide[$nlin][$e] = "<input type='hidden' name='password' value='".$linha_desc[$nlin][$e]."'>";
		}                          
	elsif(lc($linha_desc[$nlin][$e]) =~ m/^http/)
		{
		$linha_hide[$nlin][$e] = "<input type='hidden' name='".lc($titulo_desc[$e])."' value='".lc($linha_desc[$nlin][$e])."'>";
		$linha_hide[$nlin][$e] = "<input type='hidden' name='acesso' value='".lc($linha_desc[$nlin][$e])."'>";
		}
	else
		{
		$linha_hide[$nlin][$e] = "<input type='hidden' name='".lc($titulo_desc[$e])."' value='".lc($linha_desc[$nlin][$e])."'>";
		}
	}
