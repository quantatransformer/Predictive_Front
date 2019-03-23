$(function(){
    $('#btn1_1').click(function(){
        $('#icon').addClass('fa fa-refresh fa-spin fa-2x');
        $('#text').innerHTML = 'loading';
        $('#3').addClass('inner');
    });
    $("#btn2").click(function(){
        $('#icon').removeClass('fa fa-refresh fa-spin fa-2x');
    })
});
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
async function remove_1()
{
	var p2 = document.getElementById("text");
	var bar = document.getElementById('progress-bar')

	p2.innerHTML = 'Loading...'
	await sleep(1800)
	bar.setAttribute('style','width:55%')
	p2.innerHTML = 'Fitting LightGBM model ...'
	await sleep(2000)
	p2.innerHTML = 'Predicting...'
		bar.setAttribute('style','width:90%')
}
 window.onload = function()
{
	var btn1_0 = document.getElementById("btn1_0");
	btn1_0.onclick = remove_1;
}
