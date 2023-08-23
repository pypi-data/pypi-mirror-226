import 'dart:convert';
import 'dart:html';
import 'dart:js' as js;
import 'dart:math';

log(msg) {
  print(msg);
}

void main(List<String> args) async {
  //初始化列表
  js.context.callMethod("init", [args]);

  var res = await check();
  log("请求返回数据：$res");
  onHandler(res);
  //调用js的方法来操作
  js.context.callMethod('onCheck', [res]);
}

onHandler(res) {
  var code = res["code"].toString();

  if (code != 'pass' && code != '200') {
    //不通过
    var msg = res["msg"];
    //弹出提示
    // window.alert(msg);
  }
  //如果是error，就显示警告
  //其他状态码就显示激活页面
  if (code == 'error') {
    //显示警告
    log("显示警告");
  } else if (code == "404") {
    //显示激活页面
    log("显示激活页面");
    js.context.callMethod("showManifest", [res]);
  }
}

check() async {
  //localhost和127.0.0.1不做校验
  var host = window.location.hostname;

  // if (host == "localhost" || host == "127.0.0.1") {
  //   return {
  //     "code": "pass",
  //   };
  // }
  var data = {
    "host": host,
    "state": DateTime.now().millisecondsSinceEpoch,
    //安全秘钥
    "secretKey": js.context.callMethod('getSecretKey'),
  };

  //base64编码
  var str = JsonEncoder().convert(data);

  var server = 'aHR0cHM6Ly93d3cubWxkb28uY29tL3Bhc3Nwb3J0Lw==';
  //base64解码
  var domain = window.atob(server);
  var b64 = window.btoa(str);
  log("data:$str");
  log("base64:$b64");
  //http请求
  var url = domain + b64;
  log("请求的数据：$url");
  try {
    var request = await HttpRequest.request(url);
    log(request.responseText);

    var text = request.responseText;
    //转为json
    var json = JsonDecoder().convert(text!);
    return json;
  } catch (e) {
    log(e);
    return {
      "code": "error",
    };
  }
}
