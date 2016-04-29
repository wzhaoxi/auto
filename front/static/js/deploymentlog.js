$(function () {
  var xhrurl="http://127.0.0.1:8080/job/userfor/158/consoleText";

//  remoteget();
  $.ajax({
          type : "get",
          url :xhrurl,
          cache : false,
          contentType : 'text/plain', //不会执行OPTIONS预请求
  //        dataType: 'text',
          jsonp: 'jsoncallback',
          beforeSend: function (xhr) {
            xhr.setRequestHeader("If-Modified-Since", "0");
            xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
          },
          success : function(json){
              alert(json);
            },
            error:function(e){
              alert("error"+e);
            }
    });

  $.get("/api/log/136/", function(result){
    $("#console").append(result.log);
  //  alert(result);
  });
  function remoteget(){
    var xhrurl="http://127.0.0.1:8080/job/userfor/158/consoleText";
    var scriptTag=document.createElement("script");
    scriptTag.src=xhrurl;
    head = document.getElementsByTagName("head");
    if(head && head[0]){
      head[0].appendChild(scriptTag);
    }
  //  alert(data);
  };

    function iFrameHeight() {  
      var ifm= document.getElementById("iframepage");  
      var subWeb = document.frames ? document.frames["iframepage"].document : ifm.contentDocument;  
      if(ifm != null && subWeb != null) {
           ifm.height = subWeb.body.scrollHeight;
           ifm.width = subWeb.body.scrollWidth;
      }  
    };




});
