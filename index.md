<html><center>
  
<script>

function goToPage(e) {
  let url="https://raw.githubusercontent.com/LouHeb/Cado/main/"+e.target.value+".jpg";  
  console.log(url);
  window.location = url;
}
</script>


Type page number and press enter
<input onchange="goToPage(event)">  
  
</center></html>
