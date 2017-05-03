function init(){
    data={
        "method":"line_test",
        "data":{
            "type":"line",
            "step_count":7,
            "step":60*24,
            "legend_datas":["保宝点击量"],
            "title_text":"保宝网数据统计-点击量"
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