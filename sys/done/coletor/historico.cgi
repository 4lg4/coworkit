#!/usr/bin/perl

$nacess = '66';
require "../../cfg/init.pl";

$data_ini = &get('hst_data_ini');
$data_fim = &get('hst_data_fim');


# corrige datas para pesquisa --
$orderby = "coletor_relatorio.codigo desc";
if($data_ini ne "")
	{
	$DATAY = substr($data_ini, 6, 4);
	$DATAM = substr($data_ini, 3, 2);
	$DATAD = substr($data_ini, 0, 2);
	$DATA_ini = $DATAY."-".$DATAM."-".$DATAD;
	$DATA_ini_c = $DATAY."".$DATAM."".$DATAD;
	}
if($data_fim ne "")
	{
	$DATAY = substr($data_fim, 6, 4);
	$DATAM = substr($data_fim, 3, 2);
	$DATAD = substr($data_fim, 0, 2);
	$DATA_fim = $DATAY."-".$DATAM."-".$DATAD;
	$DATA_fim_c = $DATAY."".$DATAM."".$DATAD;
	}
if($data_ini ne "" && $data_fim ne "")
	{
	if($DATA_ini_c > $DATA_fim_c)
		{ 
		$DATA_ini2 = $DATA_fim;
		$DATA_fim = $DATA_ini; 
		$DATA_ini = $DATA_ini2;
		}
	}

# monta SQL dos filtros
$sqlplus = "";
if($DATA_ini ne "")
      {
      $sqlplus .= " and to_char(coletor_relatorio.data, 'YYYY-MM-DD') >= '".$DATA_ini."' ";
      }
if($DATA_fim ne "")
      {
      $sqlplus .= " and to_char(coletor_relatorio.data, 'YYYY-MM-DD') <= '".$DATA_fim."' ";
      }


print $query->header({charset=>utf8});

# lista coletores do dia / Mes ------------------------------------------------------------------------------

# zera variavel de retorno
my $R;
my $R_;

# sql exec
$DB = $dbh->prepare("select coletor_relatorio.*, empresa.nome as cliente_nome, usuario.nome as usuario_nome from coletor_relatorio left join empresa on (empresa.codigo = coletor_relatorio.cliente) left join usuario on (usuario.usuario = coletor_relatorio.usuario) where coletor_relatorio.parceiro = '$LOGEMPRESA' $sqlplus order by $orderby limit 1000");
$DB->execute;
if($dbh->err ne "") { &erroDBH($msg{db_select}." Lista de Relatorios !!!"); &erroDBR; }		

while($relatorio = $DB->fetchrow_hashref)
	{				
	# Data Ajusta
	#$relatorio->{data} = &dateToShow($relatorio->{data}); # ajusta time stamp		
	
	# Hora servidor 
	if($relatorio->{tipo} eq "noservidor")
		{ $relatorio->{tipo} = "Sem servidor"; }
	elsif($relatorio->{tipo} eq "servidor")
		{ $relatorio->{tipo} = "<b>Servidor</b>";  }
	else
		{ $relatorio->{tipo} = "Misto"; }
		
	# Cliente lenght
	if(length($relatorio->{cliente_nome}) > 30)
		{ $relatorio->{cliente_nome} = substr($relatorio->{cliente_nome}, 0, 30)."..."; }
		
	# Usuario lenght
	if(length($relatorio->{usuario_nome}) > 15)
		{ $relatorio->{usuario_nome} = substr($relatorio->{usuario_nome}, 0, 15)."."; }
	
	if($relatorio->{cliente} == NULL)
		{ $relatorio->{cliente_nome} = "Clientes Avulso"; }
	
	# Solicitante lenght
	#if(length($coletor->{solicitante}) > 20)
	#	{ $coletor->{solicitante} = substr($coletor->{solicitante}, 0, 20)."..."; }
		
	# Descrp lenght
	$relatorio->{obs} = &get($relatorio->{obs}, "NEWLINE_SHOW");
	if(length($relatorio->{obs}) > 70)
		{ $relatorio->{obs} = substr($relatorio->{obs}, 0, 70)."..."; }
	
	$R_ .= "<tr id='rel_$relatorio->{codigo}' onClick='relatorioPrint($relatorio->{codigo});' style='cursor:pointer; height:23px;'>";
	$R_ .= "	<td style='text-align:center;'>".(&dateToShow($relatorio->{data}))."</td>";
	$R_ .= "	<td style='padding-left:4px;'>$relatorio->{usuario_nome}</td>";
	$R_ .= "	<td style='padding-left:4px; text-align:center;'>".(&dateToShow($relatorio->{data_ini},"DATE"))."</td>";
	$R_ .= "	<td style='padding-left:4px; text-align:center;'>".(&dateToShow($relatorio->{data_fim},"DATE"))."</td>";
	$R_ .= "	<td style='padding-left:4px;'>$relatorio->{cliente_nome}</td>";
	$R_ .= "	<td style='padding-left:4px;'>$relatorio->{obs} </td>";
	$R_ .= "	<td style='padding-left:4px; text-align:center;'>$relatorio->{tipo} </td>";
	$R_ .= "</tr>";
	}

# header da tabela
$THEAD  = "	<thead>";
$THEAD .= "	<tr><th style='padding:2px; width:10%;'>Data</th>";
$THEAD .= "		<th style='padding:2px; width:8%;'>Usuário</th>";
$THEAD .= "		<th style='padding:2px; width:10%;'>Data Inicial</th>";
$THEAD .= "		<th style='padding:2px; width:10%;'>Data Final</th>";
$THEAD .= "		<th style='padding:2px; width:15%;'>Cliente</th>";
$THEAD .= "		<th style='padding:2px;'>Descrição</th>";
$THEAD .= "		<th style='padding:2px; width:7%;'>Tipo Rel.</th>";
$THEAD .= "	</tr>";
$THEAD .= "	</thead>";

# monta visualizacao	
$R  = "<table id='relatorio_list_tb' cellspacing='1' cellpadding='1' class='navigateable' style='width:100%;'>";
$R .= $THEAD;
$R .= "	<tbody style='width:100%; '>";
$R .= "	".$R_."";
$R .= "	</tbody>";
$R .= "</table>";	


print $R;

print<<HTML;
	<script>
	\$('#relatorio_list').show();
	</script>
HTML

exit;
