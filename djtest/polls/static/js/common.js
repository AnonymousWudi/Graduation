// JavaScript Document
$(function(){
	$.Huitab("#page-websafecolor .colortab span","#page-websafecolor .colorcon","selected","click","0");
	$.Huitab("#tab_demo .tabBar span","#tab_demo .tabCon","current","click","0");
	$.Huitab("#tab_demo2 .tabBar span","#tab_demo2 .tabCon","current","mousemove","1");
	$.Huitab("#bgpic .colortab span","#bgpic .colorcon","selected","click","0");

	/*新窗口查看代码*/
	$.Huihover('.codeView');
	/*菜单处于当前状态*/
	var webSite ="http://www.h-ui.net/";
	var loc=location.href;var url = loc.replace(webSite,"");
	$(".menu_dropdown ul li").each(function(){var current = $(this).find("a");$(this).removeClass("current");if(url == $(current[0]).attr("href")){$(this).addClass("current");}});
	
	/*返回顶部调用*/
	$(window).on("scroll",$backToTopFun);
	$backToTopFun();
}); 