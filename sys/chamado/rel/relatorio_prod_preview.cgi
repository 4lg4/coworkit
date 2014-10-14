#!/usr/bin/perl

$nacess = '40';
require "../../cfg/init.pl";


$ID = &get('ID');

# cliente
$filter_cliente = &get('filter_cliente_radios');
$cliente_cod    = &get('cliente');
$cliente_descrp = &get('cliente_descrp');

# cliente especifico
if($filter_cliente eq "especifico") {
    $cliente = " e.codigo = $cliente_cod ";
    $titulo_nome = $cliente_descrp;
} elsif($filter_cliente eq "mensalista") { # clientes mensalistas
    $cliente = " er.relacionamento = 6 ";
} elsif($filter_cliente eq "avulso") { # clientes avulsos
    $cliente = " (er.relacionamento is null or er.relacionamento = 2) ";
} else {
    $cliente = " (er.relacionamento is null or er.relacionamento is not null) ";
}
		
# 	$cliente_sql = "where ".$cliente_sql;


# tecnico
$filter_tecnico = &get('filter_tecnico_radios');
if($filter_tecnico ne "") {
	$tecnico = " and c.tecnico = $filter_tecnico ";
}
			
# periodo / datas
$filter_period = &get('filter_period_radios');
$period_ini    = &dateToSave(&get('filter_period_ini'),"DATE");
$period_end    = &dateToSave(&get('filter_period_end'),"DATE");

if($filter_period eq "period") {
	# deve haver pelo menos uma data preenchida
	if($period_ini ne "" || $period_end ne "")
		{
		# verifica se data ini ou end estao vazias e ajusta
		if($period_ini eq "")
			{ $period_ini = $period_end; }
		elsif($period_end eq "")
			{ $period_end = $period_ini; }
		
		# testa se entre datas esta invertido
		if($period_ini > $period_end)
			{
			$period_end_tmp = $period_end;
			$period_end = $period_ini;
			$period_ini = $period_end_tmp;
			}
	
		# monta filtro entre datas
		$entre_datas = " and (to_char(c.data_execucao, 'YYYY-MM-DD') >= '".$period_ini."' and to_char(c.data_execucao, 'YYYY-MM-DD') <= '".$period_end."') ";
		$titulo_datas =  &get('filter_period_ini')." - ".&get('filter_period_end');
		}
} elsif($filter_period eq "this_month") {
	$entre_datas = " and (to_char(c.data_execucao, 'YYYY-MM')  = '".timestamp("year")."-".timestamp("month")."') ";
	$titulo_datas = $DATA_MES[timestamp("month")]." de ".timestamp("year");
} elsif($filter_period eq "past_month") {
	$entre_datas = " and (to_char(c.data_execucao, 'YYYY-MM')  = to_char('".timestamp("year")."-".timestamp("month")."' - interval '1 month', 'YYYY-MM')) ";
	$titulo_datas = $DATA_MES[timestamp("month")-1];
} elsif($filter_period eq "week") {
	$DB = DBE("select ((date_trunc('week',current_date)::date) - 1) as first_day, ((date_trunc('week',current_date)::date) + 5) as last_day");
	$d = $DB->fetchrow_hashref;
	$entre_datas = " and (to_char(c.data_execucao, 'YYYY-MM-DD') >= '".$d->{first_day}."' and to_char(c.data_execucao, 'YYYY-MM-DD') <= '".$d->{last_day}."') ";
	$titulo_datas = &dateToShow($d->{first_day})." - $d->{first_day} - $d->{last_day} - ".&dateToShow($d->{last_day},"DATE");
}

# configuracao acentuacao
$dbh->do("SET CLIENT_ENCODING TO 'WINDOWS-1254'");


# joins
$join = " left join usuario as u on u.usuario = c.executor left join empresa as e on e.codigo = c.tkt_empresa left join empresa_relacionamento as er on er.empresa = e.codigo ";

# print $query->header({charset=>utf8});

# relatorio por tecnicos
$DBtec = &DBE("select u.nome as executor, count(c.tkt) as chamados, sum(c.tempo) as tempo_executado from tkt_acao_tkt as c $join where $cliente $tecnico $entre_datas group by u.nome order by u.nome asc");
# $Ttec = $DB->fetchrow_hashref();

# relatorio por tecnicos, por tipo
$DBtec_tipo = &DBE("select u.nome as executor, c.tipo_descrp as tipo, count(c.tkt) as chamados, sum(c.tempo) as tempo_executado from tkt_acao_tkt as c $join where $cliente $tecnico $entre_datas group by u.nome, c.tipo_descrp order by u.nome asc");
# $Ttec_tipo = $DB->fetchrow_hashref();

# relatorio por empresa
$DBemp = &DBE("select tkt_empresa_nome as empresa, count(c.tkt) as chamados, sum(c.tempo) as tempo_executado from tkt_acao_tkt_full as c $join where $cliente $tecnico $entre_datas group by c.tkt_empresa_nome order by c.tkt_empresa_nome asc");
# $Temp = $DB->fetchrow_hashref();

# relatorio por empresa, por tecnico
$DBemp_tec = &DBE("select tkt_empresa_nome as empresa, c.usuario_nome as tecnico, count(c.tkt) as chamados, sum(c.tempo) as tempo_executado from tkt_acao_tkt_full as c $join where $cliente $tecnico $entre_datas group by c.tkt_empresa_nome, c.usuario_nome order by c.tkt_empresa_nome, c.usuario_nome asc");
# $Temp_tec = $DB->fetchrow_hashref();

# relatorio por empresa, por tipo
$DBemp_tipo = &DBE("select tkt_empresa_nome as empresa, c.tipo_descrp as tipo, count(c.tkt) as chamados, sum(c.tempo) as tempo_executado from tkt_acao_tkt_full as c $join where $cliente $tecnico $entre_datas group by c.tkt_empresa_nome, c.tipo_descrp order by c.tkt_empresa_nome, c.tipo_descrp asc");
# $Temp_tipo = $DB->fetchrow_hashref();

# relatorio por tipo
$DBtipo = &DBE("select c.tipo_descrp as tipo, count(c.tkt) as chamados, sum(c.tempo) as tempo_executado from tkt_acao_tkt as c $join where $cliente $tecnico $entre_datas group by c.tipo_descrp order by c.tipo_descrp asc");
# $Ttipo = $DB->fetchrow_hashref();


# -- Total de atendimento por técnico mês
# -- select u.nome as Executor, count(c.codigo) as Chamados, sum(c.tempo_agendamento) as Tempo_Executado, sum(c.tempo_faturado) as Tempo_Faturado from chamado as c left join usuario as u on u.usuario = c.tecnico where to_char(c.data, 'YYYY-MM') = '2013-07' group by u.nome order by u.nome asc

# -- Total de atendimento por técnico dia
# -- select u.nome as Executor, count(c.codigo) as Chamados, sum(c.tempo_agendamento) as Tempo_Executado, sum(c.tempo_faturado) as Tempo_Faturado from chamado as c left join usuario as u on u.usuario = c.tecnico where to_char(c.data, 'YYYY-MM-DD') = '2013-07-10' group by u.nome order by u.nome asc

# -- Total de atendimentos tecnico por periodo
# -- select u.nome as Executor, count(c.codigo) as Chamados, sum(c.tempo_agendamento) as Tempo_Executado, sum(c.tempo_faturado) as Tempo_Faturado from chamado as c left join usuario as u on u.usuario = c.tecnico where to_char(c.data, 'YYYY-MM-DD') >= '2013-07-10' and to_char(c.data, 'YYYY-MM-DD') <= '2013-07-20' group by u.nome order by u.nome asc

# -- Total de atendimentos por cliente, por periodo
# -- select e.nome as Empresa, count(c.codigo) as Chamados, sum(c.tempo_agendamento) as Tempo_Executado, sum(c.tempo_faturado) as Tempo_Faturado from chamado as c left join empresa_endereco as ee on ee.codigo = c.cliente_endereco left join empresa as e on e.codigo = ee.empresa where to_char(c.data, 'YYYY-MM-DD') = '2013-07-10' group by e.nome order by chamados, e.nome asc

# -- Total de atendimentos por cliente endereco, por periodo
# -- select e.nome as Empresa, ee.endereco as Endereco, count(c.codigo) as Chamados, sum(c.tempo_agendamento) as Tempo_Executado, sum(c.tempo_faturado) as Tempo_Faturado from chamado as c left join empresa_endereco as ee on ee.codigo = c.cliente_endereco left join empresa as e on e.codigo = ee.empresa where to_char(c.data, 'YYYY-MM-DD') = '2013-07-10' group by e.nome, ee.endereco order by chamados, e.nome asc

# -- Total de atendimentos por cliente, por tipo
# -- select e.nome as Empresa, t.descrp as Tipo, count(c.codigo) as Chamados, sum(c.tempo_agendamento) as Tempo_Executado, sum(c.tempo_faturado) as Tempo_Faturado from chamado as c left join empresa_endereco as ee on ee.codigo = c.cliente_endereco left join empresa as e on e.codigo = ee.empresa left join chamado_tipo as t on t.codigo = c.tipo where to_char(c.data, 'YYYY-MM-DD') = '2013-07-10' group by e.nome, t.descrp order by chamados, e.nome asc

# -- Total de atendimentos por tipo
# -- select t.descrp as Tipo, count(c.codigo) as Chamados, sum(c.tempo_agendamento) as Tempo_Executado, sum(c.tempo_faturado) as Tempo_Faturado from chamado as c left join chamado_tipo as t on t.codigo = c.tipo where to_char(c.data, 'YYYY-MM-DD') >= '2013-07-10' and to_char(c.data, 'YYYY-MM-DD') <= '2013-07-20' group by t.descrp order by t.descrp asc



return true;
