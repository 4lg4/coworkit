#!/usr/bin/perl

require "../../cfg/init.pl";
$SHOW = &get('SHOW');
if($SHOW eq "empresas")
	{
	$TABLE = "empresas_lista";
	print $query->header('application/json');
	print '[ ';

	print '{"optionValue": "emp_codigo", "optionDisplay": "Código"}, ';
	print '{"optionValue": "emp_nome", "optionDisplay": "Nome"}, ';
	print '{"optionValue": "emp_apelido", "optionDisplay": "Apelido"}, ';
	print '{"optionValue": "emp_tipo_descr", "optionDisplay": "Tipo"}, ';
	print '{"optionValue": "empresa_endereco.endereco", "optionDisplay": "Endereço"}, ';
	print '{"optionValue": "endereco_contato.fone", "optionDisplay": "Telefone"}, ';
	print '{"optionValue": "endereco_contato.email", "optionDisplay": "E-Mail"} ';

	print '] ';
	}
elsif($SHOW eq "contatos")
	{
	$TABLE = "endereco_contato";
	print $query->header('application/json');
	print '[ ';

	print '{"optionValue": "codigo", "optionDisplay": "Código"}, ';
	print '{"optionValue": "nome", "optionDisplay": "Nome do Contato"}, ';
	print '{"optionValue": "empresa", "optionDisplay": "Empresa"}, ';
	print '{"optionValue": "tipo", "optionDisplay": "Tipo"}, ';
	print '{"optionValue": "valor", "optionDisplay": "Valor"} ';
	print '] ';
	}
else
	{
	if($SHOW eq "contatos")
		{
		$TABLE = "endereco_contato";
		$SQL = " and (column_name not ilike 'endereco' and column_name not ilike 'seq') ";
		}
	elsif($SHOW eq "usuarios")
		{
		$TABLE = "usuario";
		$SQL = " and data_type ilike 'character varying' and column_name not like 'senha' ";
		}
	else
		{
		$TABLE = $SHOW;
		}
	$SQL = "select column_name, data_type, character_maximum_length, is_nullable from information_schema.columns where table_name = '$TABLE' $SQL order by ordinal_position";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv > 0)
		{
		print $query->header('application/json');
		$out = '[ ';
		while($row = $sth->fetchrow_hashref)
			{
			if($row->{'data_type'} ne "boolean")
				{
				$out .= '{"optionValue": "'.$row->{column_name}.'", "optionDisplay": "'.&traduz($row->{column_name}).'"}, ';
				}
			}
		$out =~ s/, $/ ] /;
		
		print $out;
		}
	else
		{
		print "Content-type: text/plain\n\n";
		print "Não foi possível processar $SHOW";
		}
	}