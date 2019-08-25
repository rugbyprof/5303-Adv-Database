$(document).ready(function(){ 
	//make the newsletter form sticky
	function sticky() {
		var obj = $('#sticky-sidebar');
		if ( obj.length<1) {
			return;
		}
		
		var offset = obj.offset();
		var topOffset = offset.top;
		var leftOffset = offset.left;
		var marginTop = obj.css("marginTop");
		var marginLeft = obj.css("marginLeft");
		var height = obj.height();
		
		$( window ).resize(function() {
			adjustPos();
		});
		
		$(window).scroll(function() {
			adjustPos();
		});
		
		function adjustPos() {
			var scrollTop = $(window).scrollTop();
			var doSticky = true;
			if ( $( document ).width() <1200  ) {
				doSticky = false;
			}
			
			if ( doSticky ) {
				//obj.css({
					//marginTop: 0,
					//marginLeft: leftOffset,
					//position: 'fixed',
					//top: '60px'
					//marginTop: (scrollTop)
				//});
				obj.stop().animate({ marginTop: scrollTop}, 1000);
			} else {
				/*obj.css({
					marginTop: marginTop,
					//marginLeft: marginLeft,
					//position: 'relative',
				});*/
				obj.stop().animate({ marginTop: marginTop}, 1000);
			}
			
		}
	}
	sticky();
	
	//home page popover for tutorial title
	$('.home-page-title').popover({trigger:'hover',title:'',placement:'top',container:'body'});
	
	//contact page ajax contact form
	$('.contact-form').submit(function(){
		$this = $(this);
		var btn =$this.find('.btn');
		var error = $this.find('#contact-form-error');
		var success = $this.find('#contact-form-success');
		btn.button('loading');
		
		error.hide(1);
		success.hide(1);
		$.post($this.attr('action'), $this.serialize(), function(data){
			if ( data.status==1) {
				success.text(data.msg).fadeIn('slow');
				$this.find('input[type!=submit]').val("");
				$this.find('textarea').val("");
			} else {
				error.text(data.msg).fadeIn('slow');
			}
			btn.button('reset');
		});
		
		return false;
	});

	// highlight books

	//$('#books-navi').popover({trigger:'hover',title:'',placement:'bottom',container:'body'});
	//$('#books-navi').css('border','1px solid #4cae4c');
	//$('#books-navi').css('border-bottom','2px solid #5bc0de');
});