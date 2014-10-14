#!/usr/bin/perl

$nacess = 'nocheck';
require "../cfg/init.pl";

$pesq = &get('pesq');


print "Content-type: text/html\n\n";
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>

	<table width=100% cellpadding=4 cellspacing=1 border=0 id='tbtecnico' align='left'>
		<tbody>
HTML
$SQL = "select * from usuario where tecnico is true ";
if($pesq ne "")
	{
	$SQL .= "and usuario <=> '$pesq%' or nome <=> '$pesq%' ";
	}
$SQL .= " order by nome";
$sth3 = &select($SQL);
$rv3 = $sth3->rows();
if($rv3 < 1)
	{
	print "<tr><td>Tecnicos não cadastrados</td></tr>\n";
	}
else
	{
	while($row3 = $sth3->fetchrow_hashref)
		{
		print "<tr id='".$row3->{'usuario'}."' onClick='document.forms[0].tecnico.value=\"".$row3->{'usuario'}."\";tableRefresh(\"tbtecnico\", \"".$row3->{'usuario'}."\")'><td>".$row3->{'nome'}."</td></tr>\n";
		}
	}
print<<HTML;
	</tbody>
</table>
</body></html>
HTML


exit;


