/* [INI]  Text Editor field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		Javascript
			/comum/tiny_mce/jquery.tinymce.js
		
		CSS
			/css/ui.css
			
		IMG
			/img/tiny_mce/

    Opcoes:
		Buttons
		Model (basic / basico / simple / simples) (full / completo)
		Enable
		Disable
	
	Exemplo de uso:
		Javascript:
			$("#campo_TextEditor").fieldTextEditor();
			$(".campo_TextEditor").fieldTextEditor();
			
			$("#campo_email").fieldTextEditor(
				{
				options:values
				});
							
		HTML:
			<textarea id='campo_textEditor' name='campo_textEditor'></textarea>
*/



loadCSS("/comum/jwysiwyg/jquery.wysiwyg.css");
include("/comum/jwysiwyg/jquery.wysiwyg.js"); 


(function($){
	
$.fn.fieldTextEditor = function(settings) 
	{
	var settings = $.extend(
		{
		enable		: 'on',
		model		: 'basic',
		}, settings);
	
	// return fields
	return this.each(function()
		{
		// modelo basico
		if(settings.model == "basic" || settings.model == "basico" || settings.model == "simple" || settings.model == "simples")
			{
			$(this).wysiwyg(
				{
				rmUnusedControls: true,
				controls: {
					bold          : { visible : true },
					italic        : { visible : true },
					underline     : { visible : true },
					strikeThrough : { visible : true },
					
					justifyLeft   : { visible : true },
					justifyCenter : { visible : true },
					justifyRight  : { visible : true },
					justifyFull   : { visible : true },
					
					undo : { visible : true },
					redo : { visible : true },
					
					insertHorizontalRule : { visible : true },

					h4: {
						visible: true,
						className: 'h4',
						command: ($.browser.msie || $.browser.safari) ? 'formatBlock' : 'heading',
						arguments: ($.browser.msie || $.browser.safari) ? '<h4>' : 'h4',
						tags: ['h4'],
						tooltip: 'Header 4'
					},
					h5: {
						visible: true,
						className: 'h5',
						command: ($.browser.msie || $.browser.safari) ? 'formatBlock' : 'heading',
						arguments: ($.browser.msie || $.browser.safari) ? '<h5>' : 'h5',
						tags: ['h5'],
						tooltip: 'Header 5'
					},
					
					cut   : { visible : true },
					copy  : { visible : true },
					paste : { visible : true },
					increaseFontSize : { visible : true },
					html  : { visible: true },
					decreaseFontSize : { visible : true }
				}
				});
			}
		
			
		/*
		$('#wysiwyg').wysiwyg({
		  controls: {
			bold          : { visible : true },
			italic        : { visible : true },
			underline     : { visible : true },
			strikeThrough : { visible : true },
			
			justifyLeft   : { visible : true },
			justifyCenter : { visible : true },
			justifyRight  : { visible : true },
			justifyFull   : { visible : true },

			indent  : { visible : true },
			outdent : { visible : true },

			subscript   : { visible : true },
			superscript : { visible : true },
			
			undo : { visible : true },
			redo : { visible : true },
			
			insertOrderedList    : { visible : true },
			insertUnorderedList  : { visible : true },
			insertHorizontalRule : { visible : true },

			h4: {
				visible: true,
				className: 'h4',
				command: ($.browser.msie || $.browser.safari) ? 'formatBlock' : 'heading',
				arguments: ($.browser.msie || $.browser.safari) ? '<h4>' : 'h4',
				tags: ['h4'],
				tooltip: 'Header 4'
			},
			h5: {
				visible: true,
				className: 'h5',
				command: ($.browser.msie || $.browser.safari) ? 'formatBlock' : 'heading',
				arguments: ($.browser.msie || $.browser.safari) ? '<h5>' : 'h5',
				tags: ['h5'],
				tooltip: 'Header 5'
			},
			h6: {
				visible: true,
				className: 'h6',
				command: ($.browser.msie || $.browser.safari) ? 'formatBlock' : 'heading',
				arguments: ($.browser.msie || $.browser.safari) ? '<h6>' : 'h6',
				tags: ['h6'],
				tooltip: 'Header 6'
			},
			
			cut   : { visible : true },
			copy  : { visible : true },
			paste : { visible : true },
			html  : { visible: true },
			increaseFontSize : { visible : true },
			decreaseFontSize : { visible : true },
			exam_html: {
				exec: function() {
					this.insertHtml('<abbr title="exam">Jam</abbr>');
					return true;
				},
				visible: true
			}
		  },
		  events: {
			click: function(event) {
				if ($("#click-inform:checked").length > 0) {
					event.preventDefault();
					alert("You have clicked jWysiwyg content!");
				}
			}
		  }
		});
		*/
		});

	};

})( jQuery );