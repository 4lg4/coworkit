#!/usr/bin/perl

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

$nacess = "4";
require "../cfg/init.pl";

$ID = &get('ID');

$USUARIO = &get('USUARIO');
if($USUARIO ne "")
	{
	$USUARIO_FILTRO = " or c.tecnico = $USUARIO";
	}


# ajusta agenda somente para usuario logado
$FILTRO = "where c.tecnico = $USER->{usuario} ".$USUARIO_FILTRO;

# and data_conclusao is null
print $query->header({charset=>utf8});

# [INI] Chamados, lista chamados ------------------------------------------------------------------------------------------

	$DB = &DBE("select c.*, to_char(c.data_agendamento, 'YYYY') as y, to_char(c.data_agendamento, 'MM') as m, to_char(c.data_agendamento, 'HH24') as h, to_char(c.data_agendamento, 'MI') as mi, to_char(c.data_agendamento, 'DD') as d, e.nome as cliente_nome, u.nome as tecnico_nome from chamado as c left join empresa_endereco as ee on ee.codigo = c.cliente_endereco left join empresa as e on e.codigo = ee.empresa left join usuario as u on u.usuario = c.tecnico $FILTRO");
	
	if($DB->rows() > 0)
		{
		while($e = $DB->fetchrow_hashref)
			{
			# se chamado nao for do tecnico
			$USUARIO_SHOW = "";			
			if($e->{tecnico} == $USUARIO)
				{
				$USUARIO_SHOW = "[".&slimit($e->{tecnico_nome},10,".")."]";
				}
				
			# monta array com todos os itens
			$eventos .= "{";
			$eventos .= "id: '$e->{codigo}',";
			$eventos .= "type: 'chamado',";
			$eventos .= "title: '$USUARIO_SHOW ".(&slimit($e->{cliente_nome},10,":"))." ".(&slimit(&get($e->{descrp},"NEWLINE_SHOW"),20))."',";
			$eventos .= "start: new Date('$e->{y}', (parseInt('$e->{m}')-1), '$e->{d}', '$e->{h}', '$e->{mi}'),";
			$eventos .= "end: new Date('$e->{y}', (parseInt('$e->{m}')-1), '$e->{d}', '$e->{h}', '$e->{mi}'),";
			$eventos .= "allDay: false,";
			
			# dados complementares para tooltip
 			$eventos .= "field_descrp: '".(&slimit(&get($e->{descrp},"NEWLINE_SHOW"),40))."',";
			$eventos .= "field_descrp_resolucao: '".(&slimit(&get($e->{descrp_resolucao},"NEWLINE_SHOW"),40))."',";
			$eventos .= "field_data_agendamento: '".(&dateToShow($e->{data_agendamento}))."',";
			$eventos .= "field_tempo_agendamento: '".(&dateToShow($e->{tempo_agendamento}))."',";
			$eventos .= "field_data_conclusao: '".(&dateToShow($e->{data_conclusao}))."',";
			$eventos .= "field_tempo_faturado: '".(&dateToShow($e->{tempo_faturado}))."',";
			
			# ajuste de cores dos chamados
			# se estiver em aberto
			if($e->{data_conclusao} eq "")
				{ # se nao vencido
				if(&dateToShow($e->{data_agendamento},"comparison") >= &timestamp("comparison"))
					{
					$eventos .= "className: 'agenda_event_ativo_prioridade_3',";
					}
				else # vencidos
					{
					$eventos .= "className: 'agenda_event_ativo_vencido',";
					}	
				}
			else # se estiver concluido / cancelado
				{
				$eventos .= "className: 'agenda_event_inativo',";
				}
				
			$eventos .= "},";
			}
		$eventos = substr($eventos, 0,-1); # remove ultima virgula
		}
		
# debug($eventos);

print<<HTML;

<script>


// monta calendario
\$('#dashboard_calendar').html("").fullCalendar(
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
 		// \$(this).css('border-color', 'red');

		// alert(calEvent.colorClass);
		
		// chama modulo com solicitacao de edicao
		call('chamado/edit.cgi', { COD : calEvent.id });
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
				
				var conteudo  = "<div class='agenda_tooltip'>";
					conteudo += "	<div class='agenda_tooltip_title'><span>#"+calEvent.id+"</span><span>"+calEvent.type+"</span></div>";
					conteudo += "	<div class='agenda_tooltip_time'>";
					conteudo += "		<span>"+calEvent.field_data_agendamento+" ("+calEvent.field_tempo_agendamento+")</span>";
					conteudo += "		<span>"+calEvent.field_data_conclusao+" ("+calEvent.field_tempo_faturado+")</span>";
					conteudo += "	</div>";
					conteudo += "	<div class='agenda_tooltip_descrp'>"+calEvent.field_descrp+"</div>";
					conteudo += "	<div class='agenda_tooltip_descrp2'>"+calEvent.field_descrp_resolucao+"</div>";
					conteudo += "</div>";
				
				return conteudo;
				}
			});
		}
	});

// ajusta height na tela
\$('#dashboard_calendar').fullCalendar('option', 'aspectRatio', 2);

</script>

HTML
