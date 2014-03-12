<?php
$url = $_GET["url"];
$file = file_get_contents($url);
$imagetype = exif_imagetype($url);
if ($imagetype == 1) {
	header("Content-type: image/gif");
} else if
   ($imagetype == 2) {
	header("Content-type: image/jpeg");
} else if
   ($imagetype == 3) {
	header("Content-type: image/png");
} else {
	$font = 'OpenSans-Regular.ttf'; 
	$fontSize = 18; 
	$height = 32; 
	$width = 350; 
	$str = 'Konnte das Bild nicht laden.'; 
	$img_handle = imagecreate ($width, $height) or die ("Cannot Create image"); 
	$backColor = imagecolorallocate($img_handle, 255, 255, 255); 
	$txtColor = imagecolorallocate($img_handle, 20, 92, 137);  
	$textbox = imagettfbbox($fontSize, 0, $font, $str) or die('Error in imagettfbbox function'); 
	$x = ($width - $textbox[4])/2; 
	$y = ($height - $textbox[5])/2; 
	imagettftext($img_handle, $fontSize, 0, $x, $y, $txtColor, $font , $str) or die('Error in imagettftext function'); 
	header('Content-Type: image/jpeg'); 
	imagejpeg($img_handle,NULL,100); 
	imagedestroy($img_handle);  

	exit;
}
echo $file;
?>
