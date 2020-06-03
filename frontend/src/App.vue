<template>
  <div id="app">
    <div id="contain">
        uuid: <span id="UUID"> {{uuid}}</span>
<!--        <br>-->
        <el-button style="float: left" type="primary" plain @click.native="refreshGraph">刷新散点图</el-button>

    </div>
     <scatterGraph :propData="plotInfo" divId="plot"  style="height: 800px"></scatterGraph>
     <div id="time"> {{status}}</div>
  </div>
</template>

<script>
import scatterGraph from './components/scatterGraph'
import {uuid} from 'vue-uuid'
import axios from 'axios'
export default {
  name: 'App',
  components: {scatterGraph},
  data: function () {
    return ({
      plotInfo: {
        data: [{ x: [0],
          y: [0],
          z: [0],
          name: '动画',
          type: 'scatter3d',
          mode: 'markers',
          marker: {size: 0},
          opacity: 0
        }, {
          x: [30, 50, 20, 60, 44, 88, 98, 22],
          y: [30, 50, 20, 60, 44, 88, 70, 22],
          z: [30, 50, 20, 10, 44, 19, 9, 22],
          type: 'scatter3d',
          mode: 'markers',
          showlegend: false
        }]
      },
      step: '',
      options: [],
      value: '',
      status: '',
      uuid: ''
    })
  },
  mounted () {
    console.log('app.vue mounted')
    // this.updatePlot() uuid.v1()
    this.setUuid()
  },
  methods: {
    setUuid () {
      let uid = this.$cookies.get('uuid')
      if (!uid) {
        this.uuid = uuid.v1()
        this.$cookies.set('uuid', this.uuid, 60)
        // axios.post('http://127.0.0.1:5000/api/setuuid', {
        //   'uuid': this.uuid
        // })
        //   .then((response) => {
        //     console.log(response.data)
        //     this.uuid = response.data
        //   })
        //   .catch((error) => {
        //     console.log(error)
        //   })
      } else {
        this.uuid = uid
      }
    },
    updatePlot () {
      console.log('app.vue updateplot')
      let x, y, z
      axios.post('http://127.0.0.1:5000/api/getdata', {
        'uuid': this.$cookies.get('uuid')
      }).then(res => {
        if (res.data.success) {
          console.log('获取数据成功!')
          console.log(res.data)
          x = res.data.data.x
          y = res.data.data.y
          z = res.data.data.z
          let data = [{ x: [0],
            y: [0],
            z: [0],
            name: '动画',
            type: 'scatter3d',
            mode: 'markers',
            marker: {size: 0},
            opacity: 0
          }, {
            x: x,
            y: y,
            z: z,
            type: 'scatter3d',
            name: '散点',
            mode: 'markers',
            opacity: 0.5
          }]
          let layout = {
            height: 700,
            width: 800,
            // get rid of all the extra whitespace around plots
            margin: {
              t: 25,
              b: 25,
              r: 25,
              l: 25
            },
            scene: {
              aspectmode: 'data',
              xaxis: {
                range: [0, 5000]
              },
              yaxis: {
                range: [0, 8000]
              },
              zaxis: {
                range: [0, 3000]
              }
            },
            updatemenus: [{
              type: 'buttons',
              active: 0,
              buttons: [
                {label: '开始',
                  method: 'animate',
                  args: [null,
                    {frame: {duration: 200, redraw: true},
                      fromcurrent: true,
                      mode: 'immediate',
                      transition: {duration: 300, easing: 'quadratic-in-out'}}]
                },
                {label: '暂停',
                  method: 'animate',
                  args: [[null],
                    {frame: {duration: 0, redraw: false},
                      mode: 'immediate',
                      transition: {duration: 0}}]
                }
              ]
            }],
            paper_bgcolor: '#ECEFF1'
          }
          let config = {
            // newish in plotly...auto-resizes on window resize
            responsive: true
          }
          console.log('update data', data)
          this.plotInfo = {data: data, layout: layout, config: config}
        } else {
          console.log('else')
          alert(res.data.message + ',' + res.data.data)
        }
      }).catch(err => {
        console.log('error', err)
      })
    },
    refreshGraph () {
      this.updatePlot()
      this.status = 'Plot last updated at ' + new Date()
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.scattergraph {
  margin-top: 60px;
}
.span{
  float: left;
}
#contain {
  /*float: left;*/
  margin-bottom: 10px;
  /*margin-left: 50px;*/
}
#time{
   /*margin-top: 10px;*/
}
</style>
