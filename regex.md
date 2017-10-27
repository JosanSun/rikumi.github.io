<script src='https://unpkg.com/vue@2.5.2/dist/vue.js' />

<div id='app'>
  <h1>正则表达式游乐场</h1>
  <input v-model='str' placeholder='要匹配的字符串'/>
  <input v-model='pat' placeholder='表达式'/>
  <input v-model='replace' placeholder='全部替换为'/>
  <result>
    <p v-for='item, index in result' :class='{ empty: item == "" }'>
  	  <tag>{{ index != 0 ? index != result.length - 1 ? index : '替换结果' : '查找结果' }}</tag>
  	  {{ item == '' ? '空串' : item }}
    </p>
  </result>
</div>

<script>
  new Vue({
  	el: '#app',
    data: {
      str: '',
      pat: '',
      replace: ''
    },
    computed: {
      result() {
      	return (new RegExp(this.pat, 'g').exec(this.str) || ['没找到']).concat(this.str.replace(new RegExp(this.pat, 'g'), this.replace))
      }
    }
  })
</script>

<style>
  #app {
  	-webkit-user-select: none;
  }

  #app h1 {
    color: #333;
    font-weight: normal;
  }

  #app input {
    display: block;
    width: 100%;
    margin: 10px 0;
    padding: 10px 15px;
    border-radius: 10px;
    border: 1px solid #e4e4e4;
    outline: none;
    font-family: 'Fira Code', monospace;
  }

  #app result {
    display: block;
    padding-top: 20px;
    color: #333;
  }

  #app result p tag {
  	background: #aaa;
    color: #fff;
    padding: 5px 15px;
    border-radius: 20px;
    font-family: 'Fira Code', monospace;
    box-shadow: 0 10px 20px #eee;
    margin-right: 15px;
  }

  #app result p.empty {
  	color: #ccc;
  }

  #app result p:first-child tag {
  	background: #11cdab;
  }

  #app result p:last-child tag {
  	background: #abcd11;
  }
</style>
