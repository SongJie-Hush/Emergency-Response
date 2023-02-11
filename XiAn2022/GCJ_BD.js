// BD09II：百度地图
// GCJ02：高德地图、腾讯地图
// GCJ02 to BD09II
x_pi=3.14159265358979324 * 3000.0 / 180.0;
function marsTobaidu(mars_point){
    var baidu_point={lon:0,lat:0};
    var x=mars_point.lon;
    var y=mars_point.lat;
    var z = Math.sqrt(x * x + y * y) + 0.00002 * Math.sin(y * x_pi);
    var theta = Math.atan2(y, x) + 0.000003 * Math.cos(x * x_pi);
    baidu_point.lon = z * Math.cos(theta) + 0.0065;
    baidu_point.lat = z * Math.sin(theta) + 0.006;
    return baidu_point;
}
//**************************************************************************************
// BD09II to GCJ02
var x_pi=3.14159265358979324 * 3000.0 / 180.0;
function baiduTomars(baidu_point){
    var mars_point={lon:0,lat:0};
    var x=baidu_point.lon-0.0065;
    var y=baidu_point.lat-0.006;
    var z=Math.sqrt(x*x+y*y)- 0.00002 * Math.sin(y * x_pi);
    var theta = Math.atan2(y, x) - 0.000003 * Math.cos(x * x_pi);
    mars_point.lon=z * Math.cos(theta);
    mars_point.lat=z * Math.sin(theta);
    return mars_point;
}
