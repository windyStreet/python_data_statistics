function init(){
    var arrays = new Array();
    arrays.push(1)
    arrays.push(2)
    arrays.push(3)
    arrays.pop()
    for ( var i=0 ; i < arrays.length;i++)
    {
        //alert(arrays[i])
    }
    DBCODE = getDBCODE()
    //选取的不能大于当前值。备注：如果数据未计算，应该先采用数据恢复方案，恢复数据之后再操作
    data={
        "method":"line_test",
        "data":{
            "type":"line",
            "step_count":100,
            "step":1,
            //"filter_infos":[{"key":"time","value":"2017-05-19 10:00:00.12","relation":DBCODE.GT},{"key":"time","value":"2017-05-19 11:10:12.12","relation":DBCODE.LTE}],
            "filter_infos":[],
            "legend_infos":{
                "保宝网接口调用量":
                {
                    "project_name":"YXYBB",
                    "statistic_type":"interface"
                }
//                "保宝app点击量":
//                {
//                    "project_name":"BBT",
//                    "statistic_type":"click"
//                }
            },
            "title_text":"接口调用量统计"
           }
    }
    asyncRequest(data, func1,null)
}

function func1(data)
{

    var myChart = echarts.init(document.getElementById('main'));
    if (data.code!=1)
    {
        alert(data.msg)
        return 0
    }
    // 指定图表的配置项和数据
    var option = data.result
    console.log(option)
    option['tooltip']= { trigger: 'axis'}
    option['grid']=  {left: '3%', right: '4%',bottom: '3%',containLabel: true}
    option['toolbox'] = {feature: {saveAsImage: {}}}
    option['xAxis']['type']='category'
    option['xAxis']['boundaryGap']=false
    option['yAxis']={type: 'value'}
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
function func2(data)
{
    alert(data)
    console.log(data)
}