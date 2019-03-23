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
}
async function remove()
{
	var p2 = document.getElementById("text");
	var bar = document.getElementById('progress-bar')

	p2.innerHTML = 'Loading...'
	await sleep(1800)
	bar.setAttribute('style','width:20%')
	p2.innerHTML = 'Creating CSV ...'
	await sleep(2000)
	p2.innerHTML = 'CSV Done'
		bar.setAttribute('style','width:50%')

	await sleep(600)
	p2.innerHTML = 'Data Processing ...'

	await sleep(3500)
	p2.innerHTML = 'Data Processing Finished'
		bar.setAttribute('style','width:85%')

	await sleep(600)
	p2.innerHTML = 'Loading Charts ...'
}
 window.onload = function()
{
	var btn1 = document.getElementById("btn1");
	btn1.onclick = remove;
}
