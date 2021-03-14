const data = JSON.parse(document.getElementById('data').textContent);
const changes = JSON.parse(document.getElementById('changes').textContent);
var app = new Vue({
  el: '#app',
  delimiters: ["{$", "$}"],
  data: {
    type: 'subs',
    time: 'week',
    message: 'Привет, Vue!',
    labels: [],
    label: "Подписчики",
    data: [],
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: true,
        position: 'top',
        labels: {
          boxWidth: 80,
          fontColor: 'black'
        }
      }
    },
  },
  components: {
    'LineChart': Vue.component('line-chart', {
      extends: VueChartJs.Line,
      delimiters: ["{$", "$}"],
      props: {
        label: String,
        data: Array,
        labels: Array,
        options: Object,
        time: String,
        type: String,
      },
      watch: {
        type: function (newData, oldData) {
          this.chartChange();
        },
        time: function (newData, oldData) {
          this.chartChange();
        }
      },
      methods: {
          chartChange(){
            this.data = changes[this.time]['notes']['values'][this.type];
            this.labels = changes[this.time]['notes']['dates']
            if (this.type == 'subs') this.label = 'Подписчики';
            if (this.type == 'views') this.label = 'Просмотры';
            if (this.type == 'vids') this.label = 'Количество видео';
            this.renderChart({
              labels: this.labels,
              datasets: [{
                label: this.label,
                data: this.data,
                borderColor: 'red',
                lineTension: 0.2,
                fill: false,
              }]
            }, this.options)
          }
      },
      mounted () {
        this.chartChange();
      },
    
    }),
  },
})