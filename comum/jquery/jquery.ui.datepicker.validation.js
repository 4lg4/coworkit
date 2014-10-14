﻿/* Datepicker Validation 1.0.1 for jQuery UI Datepicker 1.8.6.
   Requires Jörn Zaefferer's Validation plugin (http://plugins.jquery.com/project/validate).
   Written by Keith Wood (kbwood{at}iinet.com.au).
   Dual licensed under the GPL (http://dev.jquery.com/browser/trunk/jquery/GPL-LICENSE.txt) and 
   MIT (http://dev.jquery.com/browser/trunk/jquery/MIT-LICENSE.txt) licenses. 
   Please attribute the author if you use it. */
(function($){if($.fn.validate){$.datepicker._selectDate2=$.datepicker._selectDate;$.extend($.datepicker.regional[''],{validateDate:'Please enter a valid date',validateDateMin:'Please enter a date on or after {0}',validateDateMax:'Please enter a date on or before {0}',validateDateMinMax:'Please enter a date between {0} and {1}',validateDateCompare:'Please enter a date {0} {1}',validateDateToday:'today',validateDateOther:'the other date',validateDateEQ:'equal to',validateDateNE:'not equal to',validateDateLT:'before',validateDateGT:'after',validateDateLE:'not after',validateDateGE:'not before'});$.extend($.datepicker._defaults,$.datepicker.regional['']);$.extend($.datepicker,{_selectDate:function(a,b){this._selectDate2(a,b);var c=$(a);var d=this._getInst(c[0]);if(!d.inline&&$.fn.validate)c.parents('form').validate().element(c)},errorPlacement:function(a,b){var c=b.next('.'+$.datepicker._triggerClass);var d=false;if(c.length==0){c=b.prev('.'+$.datepicker._triggerClass);d=(c.length>0)}a[d?'insertBefore':'insertAfter'](c.length>0?c:b)},errorFormat:function(a,b,c){var d=$.datepicker._get(a,'dateFormat');$.each(c,function(i,v){b=b.replace(new RegExp('\\{'+i+'\\}','g'),$.datepicker.formatDate(d,v)||'nothing')});return b}});var k=null;$.validator.addMethod('dpDate',function(a,b,c){k=b;var d=$.datepicker._getInst(b);var f=$.datepicker._get(d,'dateFormat');try{var g=$.datepicker.parseDate(f,a,$.datepicker._getFormatConfig(d));var h=$.datepicker._determineDate(d,$.datepicker._get(d,'minDate'),null);var i=$.datepicker._determineDate(d,$.datepicker._get(d,'maxDate'),null);var j=$.datepicker._get(d,'beforeShowDay');return this.optional(b)||!g||((!h||g>=h)&&(!i||g<=i)&&(!j||j.apply(b,[g])[0]))}catch(e){return false}},function(a){var b=$.datepicker._getInst(k);var c=$.datepicker._determineDate(b,$.datepicker._get(b,'minDate'),null);var d=$.datepicker._determineDate(b,$.datepicker._get(b,'maxDate'),null);var e=$.datepicker._defaults;return(c&&d?$.datepicker.errorFormat(b,e.validateDateMinMax,[c,d]):(c?$.datepicker.errorFormat(b,e.validateDateMin,[c]):(d?$.datepicker.errorFormat(b,e.validateDateMax,[d]):e.validateDate)))});$.validator.addClassRules('dpDate',{dpDate:true});var l={equal:'eq',same:'eq',notEqual:'ne',notSame:'ne',lessThan:'lt',before:'lt',greaterThan:'gt',after:'gt',notLessThan:'ge',notBefore:'ge',notGreaterThan:'le',notAfter:'le'};$.validator.addMethod('dpCompareDate',function(a,b,c){if(this.optional(b)){return true}c=normaliseParams(c);var d=$(b).datepicker('getDate');var e=extractOtherDate(b,c[1]);if(!d||!e){return true}k=b;var f=true;switch(l[c[0]]||c[0]){case'eq':f=(d.getTime()==e.getTime());break;case'ne':f=(d.getTime()!=e.getTime());break;case'lt':f=(d.getTime()<e.getTime());break;case'gt':f=(d.getTime()>e.getTime());break;case'le':f=(d.getTime()<=e.getTime());break;case'ge':f=(d.getTime()>=e.getTime());break;default:f=true}return f},function(a){var b=$.datepicker._getInst(k);var c=$.datepicker._defaults;a=normaliseParams(a);var d=extractOtherDate(k,a[1],true);d=(a[1]=='today'?c.validateDateToday:(d?$.datepicker.formatDate($.datepicker._get(b,'dateFormat'),d,$.datepicker._getFormatConfig(b)):c.validateDateOther));return c.validateDateCompare.replace(/\{0\}/,c['validateDate'+(l[a[0]]||a[0]).toUpperCase()]).replace(/\{1\}/,d)});function normaliseParams(a){if(typeof a=='string'){a=a.split(' ')}else if(!$.isArray(a)){var b=[];for(var c in a){b[0]=c;b[1]=a[c]}a=b}return a}function extractOtherDate(a,b,c){if(b.constructor==Date){return b}var d=$.datepicker._getInst(a);var f=null;try{if(typeof b=='string'&&b!='today'){f=$.datepicker.parseDate($.datepicker._get(d,'dateFormat'),b,$.datepicker._getFormatConfig(d))}}catch(e){}f=(f?f:(b=='today'?new Date():(c?null:$(b).datepicker('getDate'))));if(f){f.setHours(0,0,0,0)}return f}}})(jQuery);