function init(){
    jso = {}
    jso["key1"]={"value":"value","relation":"relation"}
    jso["key2"]={"value":"value","relation":"relation"}
    jso["key3"]={"value":"value","relation":"relation"}

    data={
        "method":"line_test",
        "data":{
            "type":"line",
            "step_count":7,
            "step":60*24,
            "statistic_type":"click",
            //"filter":[{"key":"key","value":"value","relation":"relation"},{"key":"key","value":"value","relation":"relation"}]
            "filter":{"key1":{"value":"value","relation":"relation"},"key2":{"value":"value","relation":"relation"}}
            "legend_infos":
            {
                "保宝网点击量":
                {
                    "project_id":"YXYBB",
                    "project_name":"YXYBB",
                },
                "保宝app点击量":
                {
                    "project_id":"BBT",
                    "project_name":"BBT",
                }
            },
            "title_text":"网站点击量统计"
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