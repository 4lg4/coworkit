#!/usr/bin/perl

use Net::Google::Calendar;

$nacess = "4";
require "../cfg/init.pl";

print $query->header({charset=>utf8});

my $cal = Net::Google::Calendar->new;
$cal->login("akgleal", "ArS4rs3607201024ArS");
AIzaSyB5rDK5vWfQf4ynlz-5rUqJHa0Ju0LwZeU


for ($cal->get_events()) {
    print $_->title."\n";
    print $_->content->body."\n*****\n\n";
}

my $c;
for ($cal->get_calendars) {
    print $_->title."\n";
    print $_->id."\n\n";
    $c = $_ if ($_->title eq 'My Non Default Calendar');
}
$cal->set_calendar($c);
print $cal->id." has ".scalar($cal->get_events)." events\n";



exit; 
# everything below here requires a read-write feed
my $entry = Net::Google::Calendar::Entry->new();
$entry->title($title);
$entry->content("My content");
$entry->location('London, England');
$entry->transparency('transparent');
$entry->status('confirmed');
$entry->when(DateTime->now, DateTime->now() + DateTime::Duration->new( hours => 6 ) );


my $author = Net::Google::Calendar::Person->new();
$author->name('Foo Bar');
$author->email('foo@bar.com');
$entry->author($author);


#
# agenda.cgi
#
# lista todos os compromissos da agenda gerando eventos para calendario
#
#  {
#	id: 
#  	title: 	'event title',
#  	start: 	new Date(year, month, day, hour, min),
#  	end: 	new Date(year, month, day, hour, min),
#  	allDay: false
#  	url: 'executa'
#  },
#
exit;

# $nacess = "2";
# require "../cfg/init.pl";

$ID = &get('ID');

print $query->header({charset=>utf8});

# [INI] Chamados, lista chamados ------------------------------------------------------------------------------------------

	$DB = &DBE("select c.*, to_char(c.data_agendamento, 'YYYY') as y, to_char(c.data_agendamento, 'MM') as m, to_char(c.data_agendamento, 'HH24') as h, to_char(c.data_agendamento, 'MI') as mi, to_char(c.data_agendamento, 'DD') as d, e.nome as cliente_nome from chamado as c left join empresa_endereco as ee on ee.codigo = c.cliente_endereco left join empresa as e on e.codigo = ee.empresa");
	
	if($DB->rows() > 0)
		{
		while($e = $DB->fetchrow_hashref)
			{
			# monta array com todos os itens
			$eventos .= "{";
			$eventos .= "id: '$e->{codigo}',";
			$eventos .= "type: 'chamado',";
			$eventos .= "title: '$e->{descrp}',";
			$eventos .= "start: new Date('$e->{y}', (parseInt('$e->{m}')-1), '$e->{d}', '$e->{h}', '$e->{mi}'),";
			$eventos .= "end: new Date('$e->{y}', (parseInt('$e->{m}')-1), '$e->{d}', '$e->{h}', '$e->{mi}'),";
			$eventos .= "allDay: false,";
			$eventos .= "},";
			}
		$eventos = substr($eventos, 0,-1); # remove ultima virgula
		}
		
debug($eventos);

print<<HTML;

<script>

// monta calendario
\$('#dashboard_calendar').fullCalendar(
	{
	header: 
		{
		left: 'prev,next today',
		center: 'title',
		right: 'month,agendaWeek,agendaDay'
		},
	editable: false,
	events: [ $eventos ],
	timeFormat: 'H(:mm)',
	eventClick: function(calEvent, jsEvent, view) 
		{
		// alert('id: ' + calEvent.id+' - Tipo: ' + calEvent.type+' - Event: ' + calEvent.title);
		// alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
		// alert('View: ' + view.name);

		// change the border color just for fun
 		\$(this).css('border-color', 'red');
	    },
	eventMouseover	: function(calEvent, jsEvent, view) 
		{
		// alert('id: ' + calEvent.id+' - Tipo: ' + calEvent.type+' - Event: ' + calEvent.title);
		\$(this).tooltip(
			{
			items: "div",
			content: function()
				{ 
				var e = \$(this); 
				// conteudo de retorno do tooltip
				return 'id: ' + calEvent.id+' - Tipo: ' + calEvent.type+' - Event: ' + calEvent.title; 
				}
			});
		}
	});

// ajusta height na tela
\$('#dashboard_calendar').fullCalendar('option', 'aspectRatio', 2);

</script>

HTML
