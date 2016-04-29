/*
this is for deployHTML

*/

genDeploymentTemplate = function(items, attrs) {
  var h = "<tr " ;
  for (attr in attrs) {
       if (attrs[attr] === false) continue;
     h += ' ' + attr + '="' + attrs[attr] + '"';
   }

   var info = "";
   for (item in items) {
     if (item === "id") continue;
     info += "<td>" + items[item] + "</td>";
   }
   return h + ">" + info +"</tr>";
};

$(function () {

  var depinfo = {
    "id": "myInput",
    "type": "text",
    "value": "我也是由模版生成的~~",
    "fdsa": "heha",
    "sdf":"hells"
  };
  $.ajax({
    type: "get",
    url: "/api/deployment/",
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    success: function(datas){
      //alert(datas[1].id);
    for (data in datas) {
    //    alert(datas[data].id);
        var test = genDeploymentTemplate(datas[data],{
          id: data.id

        });
        $('#deployInfo').append(test);
      }
    },


  });

  var test = genDeploymentTemplate(depinfo,{
      id: "1",
      type: "text",
      href: "http://www.baidu.com"
  });

  $('#deployInfo').append(test);
});

$(function () {
  arr = location.pathname.split("/");
  full_url="/api/deployment/" + arr[2] + "/";
  $.ajax({
    url: full_url,
    type: 'GET',
    success: function (data) {
      $("#detail-head").text("部署完成, 日志编号: " + data['logID'] + "  ("+ data['startTime'] +" ---> " +data['created'] + ")");
      $("#detail-user").text("部署管理员： " + data['admin']);
      $("#detail-app").text("应用版本号: " + data['appversion']);
      $("#detail-code").text("代码版本： " + data['codeversion']);
      $("#detail-result").text("部署结果： " + data['status']);

    }
  });

});

$(function () {
  var dataGrid = function (ele, opt) {
      this.defaults = {
          //id
          id: "",
          //请求url
          url: null,
          //表头格式
          columns: null,
          //是否隔行变色
          isoddcolor: false,
          //是否搜索栏
          searchnation:false,
          //页显示
          pagesize: 5,
          //页索引
          pageindex: 1,
          //总页数
          totalpage: 2
      }
      this.settings = $.extend({}, this.defaults, opt);
  }

  dataGrid.prototype = {
    _id:null,
    _op:null,
    init: function () {
        this._id=this.settings.id;
        _op=this;
        this.create();
        //绑定事件
        this.bindEvent();
    },
    create: function() {
      //初始化元素
      this.InitializeElement();
      //初始化表头
      this.createTableHead();
      this.createTableBody(1);
      this.createTableFoot();

    },
    //初始化元素
    InitializeElement: function () {
        //var id = this.settings.id;
       $("#"+this._id).empty().append("<thead><tr></tr></thead><tbody></tbody><TFOOT></TFOOT>");
    },
    //添加表头
    createTableHead: function () {
        var headcols = this.settings.columns;
        for (var i = 0; i < headcols.length; i++) {
          $("table[id='" + this._id + "'] thead tr").append("<th width=" + headcols[i].width + " align=" + headcols[i].align + ">" + headcols[i].title + "</th>");
        }
    },
    //初始化分页
    createTableFoot: function () {
        var footHtml = "<tr><td>";
        footHtml += "<span id='countPage'>第<font id='currentpageIndex'>1</font>/" +  _op.settings.totalpage + "页</span>";
        footHtml += "<span id='firstPage'>首页</span>";
        footHtml += "<span id='UpPage'>上一页</span>";
        footHtml += "<span id='nextPage'>下一页</span>";
        footHtml += "<span id='lastPage'>末页</span>";
        footHtml += "<input type='text'/><span id='skippage'>跳转</span>";
        footHtml += "</td></tr>";
        $("table[id='" + this._id + "'] tfoot").append(footHtml);
        $("table[id='" + this._id + "'] tfoot tr td").attr("colspan", "5");
    },

    createTableBody: function (pn) {
        var columns =  _op.settings.columns;
        var json = this.getAjaxDate( _op.settings.url, pn);
        //总页数
         _op.settings.totalpage = json.totalpage;
        var rowsdata = "";
        for (var row = 0; row < this.settings.pagesize; row++) {
            if (row == json.rows.length) break;
            var shift = "'/detail/" + json.rows[row].id + "/'"
            rowsdata += '<tr id= ' + json.rows[row].id + ' onclick="parent.location='+ shift+'">';
            for (var colindex = 0; colindex < columns.length; colindex++) {
              rowsdata += '<td align=left>' + json.rows[row][columns[colindex].field] + '</td>';
            }
            rowsdata += "</tr>";
        }
        $("table[id='" + this._id + "'] tbody").empty().append(rowsdata);
        $("#currentpageIndex").html(pn);
  //      this.registermousehover();
    },
    bindEvent: function () {
      //首页
      this.registerFirstPage();
      //上一页
      this.registerUpPage();
      //下一页
      this.registerNextPage();
      //尾页
      this.registerlastPage();
      //页面跳转
      this.registerSkipPage();
    },

    //首页事件
    registerFirstPage: function () {
        $("#firstPage").click(function(){
            _op.settings.pageindex = 1;
            _op.createTableBody( _op.settings.pageindex);
        });
    },
    //上一页事件
    registerUpPage: function () {
        $("table").delegate("#UpPage", "click",
        function () {
            if ( _op.settings.pageindex == 1) {
                alert("已经是第一页了");
                return;
            }
            _op.settings.pageindex =  _op.settings.pageindex - 1;
            _op.createTableBody(_op.settings.pageindex);
        });
    },

    //下一页事件
    registerNextPage: function () {
        $("table").delegate("#nextPage", "click",
        function () {
            if (_op.settings.pageindex == _op.settings.totalpage) {
                alert("已经是最后一页了");
                return;
            }
            _op.settings.pageindex = _op.settings.pageindex + 1;
            _op.createTableBody(_op.settings.pageindex);
        });
    },
    //尾页事件
    registerlastPage: function () {
        $("table").delegate("#lastPage", "click",
        function () {
             _op.settings.pageindex =  _op.settings.totalpage;
            _op.createTableBody( _op.settings.totalpage);
        });
    },
    //页数跳转事件
    registerSkipPage: function () {
        $("table").delegate("#skippage", "click",
        function () {
            var value = $("table[id='" + this._id + "'] tfoot tr td input").val();
            alert(value);
            if (!isNaN(parseInt(value))) {
                if (parseInt(value) <=  _op.settings.totalpage) _op.createTableBody(parseInt(value));
                else alert("超出页总数");
            } else alert("请输入数字");
        });
    },

    getAjaxDate: function (url, parm) {
        //定义一个全局变量来接受$get的返回值
        var result;
        //用ajax的同步方式
        full_url = url + "?page=" + parm
        $.ajax({
            url: full_url,
            async: false,
            //改为同步方式
            data: parm,
            success: function (data) {
                result = data;
            }
        });
        return result;
    }


  }


  $.fn.grid = function (options) {
      var grid = new dataGrid(this, options);
      return this.each(function () {
          grid.init();
      });
  }

  $("#myTable").grid({
          id:"myTable",
          url:"/api/deployment/",
          columns: [
  //                     {field:'ck',checkbox:true},
  //                     { field: 'ID', title: '创建时间', width:100, align: 'center'},

                       { field: 'created', title: '创建时间', align: 'center'},
                       { field: 'appversion', title: '应用版本', align: 'center' },
                       { field: 'codeversion', title: '代码版本', align: 'center' },
                       { field: 'status', title: '结果', align: 'center' },
                       { field: 'admin', title: '管理员', align: 'center' }
                   ],
          isoddcolor:false,
          searchnation:true,
          pagesize:10
      });


});





$(function () {
  $("#dep_situation").click(function(){
    arr = location.pathname.split("/");
    full_url="/api/deployment/" + arr[2] + "/";
    $.ajax({
      url: full_url,
      type: "GET",
      success: function (data) {
        alert(data);
      }
    });
    alert(full_url);


  });

  $("#dep_log").click(function(){

    $.get("/api/log/121/", function(result){
      $("#console").html(result);
    //  alert(result);
    });


  });

  $("#dep_delete_button").click(function(){
    arr = location.pathname.split("/");
    full_url="/api/deployment/" + arr[2] + "/";
    $.ajax({
      url: full_url,
      type: 'DELETE',
      beforeSend: function(request) {
        request.setRequestHeader('X-CSRFToken',getCookie('csrftoken'));
      },
      success: function (data) {
        window.location.href='/dep_history/';
      }
    });

  });

  function getCookie(name) {
       var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
       if(arr=document.cookie.match(reg))
           return unescape(arr[2]);
       else
           return null;
  }

});
