// 		$('#mask_div').show_mask();
// 		$('#mask_div').show_mask("{'background-color': 'yellow', 'z-index': '10000'}");
// 		$('#mask_div').hide_mask();

$(function()
{
	if ( $('#mask_div').attr('id') == undefined )
		$('body').append('<div id="mask_div"></div>');

	$('#mask_div').hide().css({'background-color':'white','width':'100%','height': '100%','position':'fixed','left':'0','top':'0'});
	setOpacity ($('#mask_div'),0.5);
	function setOpacity (element,alpha)
	{
		var style = element[0].style;

		if( style.MozOpacity != undefined ){	//Moz and older
			style.MozOpacity = alpha;
		}else if( style.opacity != undefined ){	//Opera
			style.opacity = alpha;

		}else if( style.filter != undefined ){  //IE
			style.filter = "alpha(opacity=0)";
			element[0].filters.alpha.opacity = ( alpha * 100 );
		}
	}

	$.fn.show_mask = function (css_setting)
	{
		$('#mask_div').show();
		if(typeof css_setting != 'undefined')
			$('#mask_div').css(css_setting);

		if (document.body.scroll != undefined)
			document.body.scroll = 'no';
		else
			$('body').css({'overflow':'hidden'});
	}

	$.fn.hide_mask = function ()
	{
		$('#mask_div').hide();
		if (document.body.scroll != undefined)
			document.body.scroll = 'auto';
		else
			$('body').css({'overflow':'auto'});
	}
});