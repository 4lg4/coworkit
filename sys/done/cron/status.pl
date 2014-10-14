#!/usr/bin/perl


return true;




sub check_msn
	{
	my ($cod, $dt, $tipo) = @_;
	if(! $tipo)
		{
		$tipo = "iconplus";
		}
	my $out = "";
	my $sth = &select("select * from cron where codigo = '$cod' limit 1");
	my $rv = $sth->rows();
	if($rv > 0)
		{
		my $row = $sth->fetchrow_hashref;
		$tmin = $row->{'tmin'}." hours";
		$tmax = $row->{'tmax'}." hours";
		}
	else
		{
		$tmin = "1 minute";
		$tmax = "12 hours";
		}
	$sth->finish;

	my $sth = &select("select *, cron_historico.dt as dt from cron_historico left join cron_historico_check on cron_historico.cron = cron_historico_check.cron and to_char(cron_historico.dt, 'YYYYMMDD') = to_char(cron_historico_check.dt, 'YYYYMMDD') where to_char(cron_historico.dt, 'YYYY-MM-DD') = '$dt' and cron_historico.cron = '$cod' and cron_historico.descrp ilike 'OK, %' order by cron_historico.dt limit 1");
	my $rv = $sth->rows();
	if($rv > 0)
		{
		my $row = $sth->fetchrow_hashref;
		if($tipo eq "status")
			{
			$out .= "Monitorando Corretamente";
			}
		elsif($tipo eq "icon")
			{
			$out .= "<img src='$dir{img_syscall}/ui/ok.png' border=0 width=25 alt='OK' title='Monitorando Corretamente' ";
			}
		else
			{
			$out .= "<img src='$dir{img_syscall}/ui/ok.png' border=0 width=25 alt='OK' title='Monitorando Corretamente' onClick='icon_reset(); get_status_ok(event, \"$cod\", \"$dt\", \"Monitorando Corretamente\"); this.src=\"$dir{img_syscall}/ui/ok_clicked.png\";' ";
			}
		}

	 if($out eq "")
		{
		$sth->finish();
		my $sth = &select("select *, cron_historico.dt as dt from cron_historico left join cron_historico_check on cron_historico.cron = cron_historico_check.cron and to_char(cron_historico.dt, 'YYYYMMDD') = to_char(cron_historico_check.dt, 'YYYYMMDD') where to_char(cron_historico.dt, 'YYYY-MM-DD') = '$dt' and cron_historico.cron = '$cod' and cron_historico.descrp ilike 'sem registros' order by cron_historico.dt limit 1");
		my $rv = $sth->rows();
		if($rv > 0)
			{
			my $row = $sth->fetchrow_hashref;
			if($tipo eq "status")
				{
				$out .= "Sem monitoramento";
				}
			elsif($tipo eq "icon")
				{
				if($row->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/critical_ok.png' border=0 width=25 alt='Sem registros' title='Sem monitoramento' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/critical.png' border=0 width=25 alt='Sem registros' title='Sem monitoramento' ";
					}
				}
			else
				{
				if($row->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/critical_ok.png' border=0 width=25 alt='Sem registros' title='Sem monitoramento' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Sem monitoramento\"); this.src=\"$dir{img_syscall}/ui/critical_clicked.png\";' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/critical.png' border=0 width=25 alt='Sem registros' title='Sem monitoramento' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Sem monitoramento\"); this.src=\"$dir{img_syscall}/ui/critical_clicked.png\";' ";
					}
				}
			}
		}

	if($out eq "")
		{
		$sth->finish();
		my $sth = &select("select *, cron_historico.dt as dt from cron_historico left join cron_historico_check on cron_historico.cron = cron_historico_check.cron and to_char(cron_historico.dt, 'YYYYMMDD') = to_char(cron_historico_check.dt, 'YYYYMMDD') where to_char(cron_historico.dt, 'YYYY-MM-DD') = '$dt' and cron_historico.cron = '$cod' order by cron_historico.dt limit 1");
		my $rv = $sth->rows();
		if($rv > 0)
			{		
			my $row = $sth->fetchrow_hashref;
			if($tipo eq "status")
				{
				$out .= "Impossível determinar execução correta";
				}
			elsif($tipo eq "icon")
				{
				if($row->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/warning_ok.png' border=0 width=25 alt='Falha' title='Falha' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/warning.png' border=0 width=25 alt='Falha' title='Falha' ";
					}
				}
			else
				{
				if($row->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/warning_ok.png' border=0 width=25 alt='Falha_ok' title='Falha' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Impossível determinar execução correta\"); this.src=\"$dir{img_syscall}/ui/warning_clicked.png\";' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/warning.png' border=0 width=25 alt='Falha' title='Falha' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Impossível determinar execução correta\"); this.src=\"$dir{img_syscall}/ui/warning_clicked.png\";' ";
					}
				}
			}
		else
			{
			my $sth3 = &select("select * from cron_historico_check where cron_historico_check.dt = '$dt' and cron_historico_check.cron = '$cod' order by cron_historico_check.dt desc limit 1");
			my $row3 = $sth3->fetchrow_hashref;
			if($tipo eq "status")
				{
				$out .= "Não executado";
				}
			elsif($tipo eq "icon")
				{
				if($row3->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/stop_ok.png' border=0 width=25 alt='Erro' title='Erro' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/stop.png' border=0 width=25 alt='Erro' title='Erro' ";
					}
				}
			else
				{
				if($row3->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/stop_ok.png' border=0 width=25 alt='Erro' title='Erro' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Não executado\"); this.src=\"$dir{img_syscall}/ui/stop_clicked.png\";' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/stop.png' border=0 width=25 alt='Erro' title='Erro' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Não executado\"); this.src=\"$dir{img_syscall}/ui/stop_clicked.png\";' ";
					}
				}
			$sth3->finish;
			}
		}
	$sth->finish();
	if($tipo eq "icon")
		{
		$out .= ">";
		}
	elsif($tipo ne "status")
		{
		$out .= "onMouseOver=\"this.style.cursor='help'\">";
		}
	return $out;
	}


# Código de checagem quando for mirror
sub check_mirror
	{
	my ($cod, $dt, $tipo) = @_;
	if(! $tipo)
		{
		$tipo = "iconplus";
		}
	my $out = "";
	my $sth = &select("select * from cron where codigo = '$cod' limit 1");
	my $rv = $sth->rows();
	if($rv > 0)
		{
		my $row = $sth->fetchrow_hashref;
		$tmin = $row->{'tmin'}." hours";
		$tmax = $row->{'tmax'}." hours";
		}
	else
		{
		$tmin = "1 minute";
		$tmax = "12 hours";
		}
	$sth->finish;

	# Traz os "cientes"
	my $sth3 = &select("select * from cron_historico_check where cron_historico_check.dt = '$dt' and cron_historico_check.cron = '$cod' order by cron_historico_check.dt desc limit 1");
	my $row3 = $sth3->fetchrow_hashref;

	# conta os inícios
	my $sth = &select("select count(*) from cron_historico left join cron_historico_check on cron_historico.cron = cron_historico_check.cron and to_char(cron_historico.dt, 'YYYYMMDD') = to_char(cron_historico_check.dt, 'YYYYMMDD') where to_char(cron_historico.dt, 'YYYY-MM-DD') = '$dt' and cron_historico.cron = '$cod' and cron_historico.descrp ilike 'iniciado' ");
	my $row = $sth->fetchrow_arrayref;
	if(@$row[0] > 0)
		{
		# conta os finalizados
		my $sth2 = &select("select count(*) from cron_historico where to_char(cron_historico.dt, 'YYYY-MM-DD') = '$dt' and cron_historico.cron = '$cod' and cron_historico.descrp ilike 'finalizado' ");
		my $row2 = $sth2->fetchrow_arrayref;
		if(@$row2[0] > 0)
			{
			# Se houver mesmo quantidade de inicios e fins
			if(@$row[0] eq @$row2[0])
				{
				if($tipo eq "status")
					{
					$out .= "Monitorando Corretamente";
					}
				elsif($tipo eq "icon")
					{
					$out .= "<img src='$dir{img_syscall}/ui/ok.png' border=0 width=25 alt='OK' title='Monitorando Corretamente' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/ok.png' border=0 width=25 alt='OK' title='Monitorando Corretamente' onClick='icon_reset(); get_status_ok(event, \"$cod\", \"$dt\", \"Monitorando Corretamente\"); this.src=\"$dir{img_syscall}/ui/ok_clicked.png\";' ";
					}
				}
			else
				{
				# se os valores não coincidirem
				if($tipo eq "status")
					{
					$out .= "Impossível determinar se foi completado corretamente";
					}
				elsif($tipo eq "icon")
					{
					if($row3->{'ciente'})
						{
						$out .= "<img src='$dir{img_syscall}/ui/warning_ok.png' border=0 width=25 alt='Falha' title='Falha' ";
						}
					else
						{
						$out .= "<img src='$dir{img_syscall}/ui/warning.png' border=0 width=25 alt='Falha' title='Falha' ";
						}
					}
				else
					{
					if($row3->{'ciente'})
						{
						$out .= "<img src='$dir{img_syscall}/ui/warning_ok.png' border=0 width=25 alt='Falha_ok' title='Falha' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Impossível determinar se foi completado corretamente\"); this.src=\"$dir{img_syscall}/ui/warning_clicked.png\";' ";
						}
					else
						{
						$out .= "<img src='$dir{img_syscall}/ui/warning.png' border=0 width=25 alt='Falha' title='Falha' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Impossível determinar se foi completado corretamente\"); this.src=\"$dir{img_syscall}/ui/warning_clicked.png\";' ";
						}
					}
				}
			}
		else
			{
			# se não houver nenhum finalizado
			if($tipo eq "status")
				{
				$out .= "Erro durante a execução";
				}
			elsif($tipo eq "icon")
				{
				if($row3->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/critical_ok.png' border=0 width=25 alt='Incompleto' title='Incompleto' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/critical.png' border=0 width=25 alt='Incompleto' title='Incompleto' ";
					}
				}
			else
				{
				if($row3->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/critical_ok.png' border=0 width=25 alt='Incompleto' title='Incompleto' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Erro durante a execução\"); this.src=\"$dir{img_syscall}/ui/critical_clicked.png\";' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/critical.png' border=0 width=25 alt='Incompleto' title='Incompleto' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Erro durante a execução\"); this.src=\"$dir{img_syscall}/ui/critical_clicked.png\";' ";
					}
				}
			}
		}
	else
		{
		# Se não houver nenhum inicializado
		if($tipo eq "status")
			{
			$out .= "Não executado";
			}
		elsif($tipo eq "icon")
			{
			if($row3->{'ciente'})
				{
				$out .= "<img src='$dir{img_syscall}/ui/stop_ok.png' border=0 width=25 alt='Erro' title='Erro' ";
				}
			else
				{
				$out .= "<img src='$dir{img_syscall}/ui/stop.png' border=0 width=25 alt='Erro' title='Erro' ";
				}
			}
		else
			{
			if($row3->{'ciente'})
				{
				$out .= "<img src='$dir{img_syscall}/ui/stop_ok.png' border=0 width=25 alt='Erro' title='Erro' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Não executado\"); this.src=\"$dir{img_syscall}/ui/stop_clicked.png\";' ";
				}
			else
				{
				$out .= "<img src='$dir{img_syscall}/ui/stop.png' border=0 width=25 alt='Erro' title='Erro' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Não executado\"); this.src=\"$dir{img_syscall}/ui/stop_clicked.png\";' ";
				}
			}
		$sth3->finish;
		}
	$sth->finish();
	if($tipo eq "icon")
		{
		$out .= ">";
		}
	elsif($tipo ne "status")
		{
		$out .= "onMouseOver=\"this.style.cursor='help'\">";
		}
	return $out;
	}


sub check
	{
	my ($cod, $dt, $tipo) = @_;
	if(! $tipo)
		{
		$tipo = "iconplus";
		}
	my $out = "";
	my $sth = &select("select * from cron where codigo = '$cod' limit 1");
	my $rv = $sth->rows();
	if($rv > 0)
		{
		my $row = $sth->fetchrow_hashref;
		$tmin = $row->{'tmin'}." hours";
		$tmax = $row->{'tmax'}." hours";
		}
	else
		{
		$tmin = "1 minute";
		$tmax = "12 hours";
		}
	$sth->finish;

	# Verifica se tem algum agendamento com a palavra iniciado no dia
	my $sth = &select("select *, cron_historico.dt as dt from cron_historico left join cron_historico_check on cron_historico.cron = cron_historico_check.cron and to_char(cron_historico.dt, 'YYYYMMDD') = to_char(cron_historico_check.dt, 'YYYYMMDD') where to_char(cron_historico.dt, 'YYYY-MM-DD') = '$dt' and cron_historico.cron = '$cod' and cron_historico.descrp ilike 'iniciado' order by cron_historico.dt limit 1");
	my $rv = $sth->rows();
	if($rv == 0)
		{
		# Refaz o SQL procurando qualquer ocorrência no dia
		$sth = &select("select *, cron_historico.dt as dt from cron_historico left join cron_historico_check on cron_historico.cron = cron_historico_check.cron and to_char(cron_historico.dt, 'YYYYMMDD') = to_char(cron_historico_check.dt, 'YYYYMMDD') where to_char(cron_historico.dt, 'YYYY-MM-DD') = '$dt' and cron_historico.cron = '$cod' order by cron_historico.dt limit 1");
		$rv = $sth->rows();
		}
	if($rv > 0)
		{
		my $row = $sth->fetchrow_hashref;
		if(lc($row->{'descrp'}) eq "iniciado")
			{
			my $sth2 = &select("select *, to_char(cron_historico.dt, 'HH24:MI') as dt_conc from cron_historico where cron_historico.dt > TIMESTAMP '".$row->{'dt'}."' + interval '$tmin' and cron_historico.dt < TIMESTAMP '".$row->{'dt'}."' + interval '$tmax' and cron_historico.cron = '$cod' and cron_historico.descrp ilike 'finalizado' order by cron_historico.dt");
			my $rv2 = $sth2->rows();
			my $row2 = $sth2->fetchrow_hashref;
			if($rv2 == 1)
				{
				if($tipo eq "status")
					{
					$out .= "Realizado com sucesso";
					}
				elsif($tipo eq "icon")
					{
					$out .= "<img src='$dir{img_syscall}/ui/ok.png' border=0 width=25 alt='Completado' title='Completado' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/ok.png' border=0 width=25 alt='Completado' title='Completado' onClick='icon_reset(); get_status_ok(event, \"$cod\", \"$dt\", \"Realizado com sucesso às ".$row2->{'dt_conc'}."h\"); this.src=\"$dir{img_syscall}/ui/ok_clicked.png\";' ";
					}
				}
			elsif($rv2 > 1)
				{
				if($tipo eq "status")
					{
					$out .= "Impossível determinar se foi completado corretamente";
					}
				elsif($tipo eq "icon")
					{
					if($row->{'ciente'})
						{
						$out .= "<img src='$dir{img_syscall}/ui/warning_ok.png' border=0 width=25 alt='Falha' title='Falha' ";
						}
					else
						{
						$out .= "<img src='$dir{img_syscall}/ui/warning.png' border=0 width=25 alt='Falha' title='Falha' ";
						}
					}
				else
					{
					if($row->{'ciente'})
						{
						$out .= "<img src='$dir{img_syscall}/ui/warning_ok.png' border=0 width=25 alt='Falha_ok' title='Falha' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Impossível determinar se foi completado corretamente\"); this.src=\"$dir{img_syscall}/ui/warning_clicked.png\";' ";
						}
					else
						{
						$out .= "<img src='$dir{img_syscall}/ui/warning.png' border=0 width=25 alt='Falha' title='Falha' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Impossível determinar se foi completado corretamente\"); this.src=\"$dir{img_syscall}/ui/warning_clicked.png\";' ";
						}
					}
				}
			else
				{
				if($tipo eq "status")
					{
					$out .= "Erro durante a execução";
					}
				elsif($tipo eq "icon")
					{
					if($row->{'ciente'})
						{
						$out .= "<img src='$dir{img_syscall}/ui/critical_ok.png' border=0 width=25 alt='Incompleto' title='Incompleto' ";
						}
					else
						{
						$out .= "<img src='$dir{img_syscall}/ui/critical.png' border=0 width=25 alt='Incompleto' title='Incompleto' ";
						}
					}
				else
					{
					if($row->{'ciente'})
						{
						$out .= "<img src='$dir{img_syscall}/ui/critical_ok.png' border=0 width=25 alt='Incompleto' title='Incompleto' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Erro durante a execução\"); this.src=\"$dir{img_syscall}/ui/critical_clicked.png\";' ";
						}
					else
						{
						$out .= "<img src='$dir{img_syscall}/ui/critical.png' border=0 width=25 alt='Incompleto' title='Incompleto' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Erro durante a execução\"); this.src=\"$dir{img_syscall}/ui/critical_clicked.png\";' ";
						}
					}
				}
			}
		else
			{
			if($tipo eq "status")
				{
				$out .= "Impossível determinar execução correta";
				}
			elsif($tipo eq "icon")
				{
				if($row->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/warning_ok.png' border=0 width=25 alt='Falha' title='Falha' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/warning.png' border=0 width=25 alt='Falha' title='Falha' ";
					}
				}
			else
				{
				if($row->{'ciente'})
					{
					$out .= "<img src='$dir{img_syscall}/ui/warning_ok.png' border=0 width=25 alt='Falha_ok' title='Falha' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Impossível determinar execução correta\"); this.src=\"$dir{img_syscall}/ui/warning_clicked.png\";' ";
					}
				else
					{
					$out .= "<img src='$dir{img_syscall}/ui/warning.png' border=0 width=25 alt='Falha' title='Falha' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Impossível determinar execução correta\"); this.src=\"$dir{img_syscall}/ui/warning_clicked.png\";' ";
					}
				}
			}
		}
	else
		{
		my $sth3 = &select("select * from cron_historico_check where cron_historico_check.dt = '$dt' and cron_historico_check.cron = '$cod' order by cron_historico_check.dt desc limit 1");
		my $row3 = $sth3->fetchrow_hashref;
		if($tipo eq "status")
			{
			$out .= "Não executado";
			}
		elsif($tipo eq "icon")
			{
			if($row3->{'ciente'})
				{
				$out .= "<img src='$dir{img_syscall}/ui/stop_ok.png' border=0 width=25 alt='Erro' title='Erro' ";
				}
			else
				{
				$out .= "<img src='$dir{img_syscall}/ui/stop.png' border=0 width=25 alt='Erro' title='Erro' ";
				}
			}
		else
			{
			if($row3->{'ciente'})
				{
				$out .= "<img src='$dir{img_syscall}/ui/stop_ok.png' border=0 width=25 alt='Erro' title='Erro' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Não executado\"); this.src=\"$dir{img_syscall}/ui/stop_clicked.png\";' ";
				}
			else
				{
				$out .= "<img src='$dir{img_syscall}/ui/stop.png' border=0 width=25 alt='Erro' title='Erro' onClick='icon_reset(); get_status(event, \"$cod\", \"$dt\", \"Não executado\"); this.src=\"$dir{img_syscall}/ui/stop_clicked.png\";' ";
				}
			}
		$sth3->finish;
		}
	if($tipo eq "icon")
		{
		$out .= ">";
		}
	elsif($tipo ne "status")
		{
		$out .= "onMouseOver=\"this.style.cursor='help'\">";
		}
	return $out;
	}
