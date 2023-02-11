function lonlatTomercator(lonlat) {
    var mercator={x:0,y:0};
    var x = lonlat.x *20037508.34/180;
    var y = Math.log(Math.tan((90+lonlat.y)*Math.PI/360))/(Math.PI/180);
    y = y *20037508.34/180;
    mercator.x = x;
    mercator.y = y;
    return mercator ;
}
function mercatorTolonlat(mercator){
    var lonlat={x:0,y:0};
    var x = mercator.x/20037508.34*180;
    var y = mercator.y/20037508.34*180;
    y= 180/Math.PI*(2*Math.atan(Math.exp(y*Math.PI/180))-Math.PI/2);
    lonlat.x = x;
    lonlat.y = y;
    return lonlat;
}
