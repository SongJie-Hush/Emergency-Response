//GCJ02：高德地图、腾讯地图
//WGS84：OSM、Google、ArcGIS Online
var PI = 3.14159265358979324;
function transformGCJ2WGS(gcjLat, gcjLon) {
    let d = delta(gcjLat, gcjLon)
    return {
      'lat': gcjLat - d.lat,
      'lon': gcjLon - d.lon
    }
  }

  function delta(lat, lon) {
    let a = 6378245.0 //  a: 卫星椭球坐标投影到平面地图坐标系的投影因子。
    let ee = 0.00669342162296594323 //  ee: 椭球的偏心率。
    let dLat = transformLat(lon - 105.0, lat - 35.0)
    let dLon = transformLon(lon - 105.0, lat - 35.0)
    let radLat = lat / 180.0 * PI
    let magic = Math.sin(radLat)
    magic = 1 - ee * magic * magic
    let sqrtMagic = Math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI)
    dLon = (dLon * 180.0) / (a / sqrtMagic * Math.cos(radLat) * PI)
    return {
      'lat': dLat,
      'lon': dLon
    }
  }
  function transformLat(x, y) {
    let ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * Math.sqrt(Math.abs(x))
    ret += (20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * Math.sin(y * PI) + 40.0 * Math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * Math.sin(y / 12.0 * PI) + 320 * Math.sin(y * PI / 30.0)) * 2.0 / 3.0
    return ret
  }
  function transformLon(x, y) {
    let ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * Math.sqrt(Math.abs(x))
    ret += (20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * Math.sin(x * PI) + 40.0 * Math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * Math.sin(x / 12.0 * PI) + 300.0 * Math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    return ret
  }


var lonArray = new Array(108.967512,109.018127,108.987693,108.951071,108.94851,108.964085,109.010071,109.012244,109.003671,109.010547,108.995121,108.93015,108.9208,108.927288,108.970212,108.977696,108.944969,108.968853,108.954487,108.964456,108.873133,108.886898,108.911883,108.942984,108.896027,108.881364,108.917818,108.963393,108.939491,108.959774,108.972593,108.992871,108.939811,108.959093,108.923294,108.979515,109.069695,109.064419,109.118767,109.115634,108.936741,109.01127,108.954522,108.924232,108.951133,108.944445,108.923493,108.986671,108.932433,108.945321,108.927928,108.926659,114.519206,108.878077,108.99875,108.879522,108.726977,108.839657,108.700491,108.841053,108.715623,108.611984,108.602879,108.607261,108.6094,108.636716,108.630051,109.337969,109.322269,109.315829,108.208584,108.223564,108.201831,108.211538,109.228135,109.215927,109.227798,109.199116,109.209032,109.20045,109.203873,109.09399,109.088863,109.000266);
var latArray = new Array(34.260315,34.250287,34.272185,34.270711,34.271503,34.260732,34.278962,34.26068,34.268694,34.248905,34.276883,34.239675,34.245615,34.241921,34.233219,34.236217,34.254539,34.241719,34.257487,34.258889,34.268317,34.258373,34.288239,34.28061,34.264288,34.245853,34.258601,34.321113,34.32283,34.333728,34.296712,34.306439,34.321253,34.351607,34.336853,34.358335,34.263818,34.282331,34.307509,34.291353,34.219569,34.195972,34.166817,34.21132,34.225791,34.176401,34.197201,34.228326,34.228387,34.161573,34.170463,34.15497,38.050227,34.158432,34.165949,34.230045,34.109555,34.142076,34.329111,34.300713,34.465641,34.111997,34.11667,34.1021,34.112315,34.108494,34.058014,34.138346,34.146942,34.15261,34.161805,34.159924,34.15478,34.153633,34.661791,34.665852,34.666273,34.372243,34.369253,34.362683,34.373473,34.534754,34.518709,34.445083);
var reallon = " ";
var reallat = " ";

for (var i=0;i<lonArray.length;i++)
{
    var coodinate = transformGCJ2WGS(latArray[i],logArray[i]);
    reallon = reallon.concat(",", coodinate.lon);
    reallat = reallat.concat(",", coodinate.lat);
}

print(reallat,reallon)