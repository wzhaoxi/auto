$(function () {
  $.ajax({
    type: "get",
    url: "/api/integrationConf/",
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    success: function(data){
      $("#int_url").attr("value",data[0].url);
      $("#int_jobname").attr("value",data[0].jobName);
      $("#int_user").attr("value",data[0].user);
      $("#int_password").attr("value",data[0].password);
    },
  });

  $.ajax({
    type: "get",
    url: "/api/deploymentConf/",
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    success: function(data){
      $("#dep_sourcepath").attr("value",data[0].sourcepath);
      $("#dep_dest_path").attr("value",data[0].dest_path);
      $("#dep_release_dir").attr("value",data[0].release_dir);
      $("#dep_webapp_name").attr("value",data[0].webapp_name);
      $("#dep_war_name").attr("value",data[0].war_name);
      $("#dep_request_domain").attr("value",data[0].request_domain);
      $("#dep_request_uri").attr("value",data[0].request_uri);
      $("#dep_current_link").attr("value",data[0].current_link);
      $("#dep_host_string").attr("value",data[0].host_string);
      $("#dep_host_passwd").attr("value",data[0].host_passwd);
    },
  });


  $("#int_button").click(function(){
    url = $("#int_url").val();
    jobname = $("#int_jobname").val();
    user = $("#int_user").val();
    password = $("#int_password").val();
    $.ajax({
      url: "/api/integrationConf/",
      dataType: "json",
      type: "post",
      data: {
        "url": url,
        "jobName": jobname,
        "user": user,
        "password": password
      },
      beforeSend: function(request) {
        request.setRequestHeader('X-CSRFToken',getCookie('csrftoken'));
      },
      success: function(data){
          window.location.href='/integration_conf/';
          // window.location.reload();
      },
      error: function(e){
        alert("异常: "+e);
      }
    });

    return false;
  });

  $("#dep_button").click(function(){
    sourcepath = $("#dep_sourcepath").val();
    dest_path = $("#dep_dest_path").val();
    release_dir = $("#dep_release_dir").val();
    webapp_name = $("#dep_webapp_name").val();
    war_name = $("#dep_war_name").val();
    request_domain = $("#dep_request_domain").val();
    request_uri = $("#dep_request_uri").val();
    current_link = $("#dep_current_link").val();
    host_string = $("#dep_host_string").val();
    host_passwd = $("#dep_host_passwd").val();
    $.ajax({
      url: "/api/deploymentConf/",
      dataType: "json",
      type: "post",
      data:{
            "sourcepath": sourcepath,
            "dest_path": dest_path,
            "release_dir": release_dir,
            "webapp_name": webapp_name,
            "war_name": war_name,
            "request_domain": request_domain,
            "request_uri": request_uri,
            "current_link": current_link,
            "host_string": host_string,
            "host_passwd": host_passwd
      },
      beforeSend: function(request) {
        request.setRequestHeader('X-CSRFToken',getCookie('csrftoken'));
      },
      success: function(data){
          window.location.href='/deployment_conf/';
      },
      error: function(e){
        alert("异常: "+e);
      }
    });
    return false;
  });

  function getCookie(name) {
       var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
       if(arr=document.cookie.match(reg))
           return unescape(arr[2]);
       else
           return null;
  }

  $.ajax({
    type: "get",
    url: "/api/codeversion/",
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    success: function(datas){
      for (temp in datas) {
      //  alert(datas[temp].version);

      $("#code_version").append("<option value="+ datas[temp].version+">"+ datas[temp].version+"</option>");
      }
    },
  });

  $("#start_deploy").click(function(){
    appversion = $("#app_version").val();
    codeversion = $("#code_version").val();
    alert(appversion+"  "+codeversion);
  });

});
