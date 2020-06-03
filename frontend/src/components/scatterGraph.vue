<template>
    <div
    class="scattergraph"
    ref="container"
    :id='divId'
    :style="{
      height: (height) +  '%',
      width: (width) + '%'
    }"/>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly'
export default {
  name: 'scattergraph',
  props: {
    propData: {
      type: Object,
      required: true
    },
    divId: {
      type: String,
      required: true
    },
    height: {
      type: Number,
      default: 100
    },
    width: {
      type: Number,
      default: 95
    }
  },
  data () {
    return {
    }
  },
  mounted () {
    console.log('scatterGraph mounted')
    console.log('divId', this.divId)
  },
  computed: {
    plotDiv () {
      return this.$refs.container
    }
  },
  created () {
    console.log('scatterGraph created')
    this.$watch('propData', function (newpro, oldpro) {
      console.log('scatterGraph watch', newpro)
      // console.log('scatterGraph watch', oldpro)
      this.propData = newpro
      this.newPlot()
    })
  },
  methods: {
    newPlot () {
      let frames = []
      console.log('newPlot this.propData', this.propData.data)
      for (let j = 0; j < this.propData.data[1].x.length; j++) {
        frames[j] = {data: [{x: [this.propData.data[1].x[j]],
          y: [this.propData.data[1].y[j]],
          z: [this.propData.data[1].z[j]],
          type: 'scatter3d',
          mode: 'markers',
          opacity: 1,
          hovertext: ['point ID: ' + j.toString()],
          hoverinfo: 'x+y+z+text',
          marker: {size: 10, color: '#C54C82'}
        }]
        }
      }
      let mydiv = this.divId
      Plotly.newPlot(this.divId, this.propData.data, this.propData.layout, this.propData.config).then(function () {
        Plotly.addFrames(mydiv, frames)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
