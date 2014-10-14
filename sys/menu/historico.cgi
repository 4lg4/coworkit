#!/usr/bin/perl

$nacess = "direct";
require "../cfg/init.pl";
$MENUCOD = &get('menu_cod');

print "Content-type: text/html; Charset=utf-8\n\n";
if($MENUCOD ne "" && $USER->{usuario} ne "")
	{
	$rv = $dbh->do("insert into last_view (tabela, usuario, codigo) values ('menu', '$USER->{usuario}', '$MENUCOD') ");
	if($dbh->err ne "")
		{
		print "Erro! <br><br> Erro número : ".$dbh->err."<br>Descrição: ".$dbh->errstr;
		exit;
		}
	}

# Mostra o menu de favoritos, mas apenas se houver mais de 4 itens
$sth = &select("select last_view.codigo, count(last_view.codigo) as total from last_view where last_view.tabela = 'menu' and last_view.usuario = '$USER->{usuario}' group by last_view.codigo order by total desc limit 8");
$rv = $sth->rows();
if($rv > 3)
	{
print<<HTML;
      <div style='position: absolute; top: 20px; right: 10px; text-align: left; z-index: 10'>
	    <ul>
		  <li class='submenu'>Favoritos</li>
		  <ul>
HTML
	while($row=$sth->fetch)
		{
		$sth2 = &select("select menu.descrp from menu where menu.codigo = '@$row[0]' ");
		while($row2=$sth2->fetch)
			{
			print "<li><a href='#'>".@$row2[0]."</a></li>";
			}
		}
print<<HTML;
		  </ul>
	    </ul>
      </div>
HTML
	}
