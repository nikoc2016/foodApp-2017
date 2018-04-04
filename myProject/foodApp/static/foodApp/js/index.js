/* 
Forked from: https://github.com/NewSignature/us-map
Instructions for use at: https://newsignature.github.io/us-map/ 
*/

$(document).ready(function() {

  $(window).resize(superResize);
  superResize();
  FoodGUI.initialize();
});

function drawMap(){
	$('#map').usmap({
  	stateStyles: {fill: '#cccccc'},
  	stateHoverStyles: {fill: 'red'},
  	stateHoverAnimation: 150,
  	click: function(event, data) {
  		FoodGUI.stateClicked(data.name);
  	},
  });
}

var FoodGUI = {

	loopPtr: 0, //0-1-2
	img1: "",
	img2: "",
	img3: "",

	initialize: function(){
		FoodGUI.cout("Program Initialized!");
		FoodGUI.cout("Click state to display most popular food.");
		FoodGUI.cout("");
	},
	stateClicked: function(e){
		FoodGUI.cout("Connecting server... State: " + e);
		// virtualDisplayFood();
		$.ajax({
			url: 'ajax/communicate/',
			data: {
				'clickedState': e
			},
			dataType: 'json',
			success: function (data) {
				if (data.valid) {
					if (data.output) {
						FoodGUI.cout(data.output);
					}
					if (data.picUrl1) {
						FoodGUI.img1 = data.picUrl1;
					}
					if (data.picUrl2) {
						FoodGUI.img2 = data.picUrl2;
					}
					if (data.picUrl3) {
						FoodGUI.img3 = data.picUrl3;
					}
					if (data.picInfo) {
						FoodGUI.updateInformation(data.picInfo);
					}
					FoodGUI.loopIMG();
				} else {
					FoodGUI.cout("Server response invalid.");
				}
			},
			timeout: function () {
				FoodGUI.cout("Server no response.");
			}
		});
	},
	updatePicture: function(url){
		$("#pictureOut").attr("src", url);
	},
	loopIMG: function(){
		if (FoodGUI.loopPtr == 0) {
			$("#pictureOut").attr("src", FoodGUI.img1);
			FoodGUI.loopPtr++;
		} else if (FoodGUI.loopPtr == 1) {
			$("#pictureOut").attr("src", FoodGUI.img2);
			FoodGUI.loopPtr++;
		} else {
			$("#pictureOut").attr("src", FoodGUI.img3);
			FoodGUI.loopPtr = 0;
		}
		setTimeout(FoodGUI.loopIMG,3000);
	},
	updateInformation: function(info){
		$("#informationOut").html(info);
	},
	cout: function(string){
		$("#console").append("> " + string + "</br>");
    	var theConsole = document.getElementById("console");
		theConsole.scrollTop = theConsole.scrollHeight;
	},
	cls: function(){
		$("#console").html("");
	},
};

function superResize() {
	var wmargin = $(window).height() * 0.015;

	$("#controlPanel").height($(window).height()*(3/4));
	$("#controlPanel").width($("#controlPanel").height()*1.8);
	$("#controlPanel").css({"top": ($(window).height() - $("#controlPanel").height()) / 2, "left": ($(window).width() - $("#controlPanel").width()) / 2});

	$("#controlPanelBody").height($("#controlPanel").height() - $(".shell-top-bar").height() - 10);
	$("#controlPanelBody").width($("#controlPanel").width());

	$("#mapRegion").css({"margin":wmargin});
	$("#mapRegion").width($("#controlPanelBody").width() * (11/20) - wmargin*2);
	$("#mapRegion").height($("#controlPanelBody").height() * (5/8) - wmargin*2);

	$("#consoleRegion").css({"margin":wmargin});
	$("#consoleRegion").width($("#controlPanelBody").width() * (11/20) - wmargin*2);
	$("#consoleRegion").height($("#controlPanelBody").height() * (3/8) - wmargin*2);

	$("#picRegion").css({"margin":wmargin});
	$("#picRegion").width($("#controlPanelBody").width() * (9/20) - wmargin*2);
	$("#picRegion").height($("#controlPanelBody").height() * (5/8) - wmargin*2);

	$("#infoRegion").css({"margin":wmargin});
	$("#infoRegion").width($("#controlPanelBody").width() * (9/20) - wmargin*2);
	$("#infoRegion").height($("#controlPanelBody").height() * (3/8) - wmargin*2);

	drawMap();
}