<template>
  <div id="footer">
    <p>{{copyRight}}</p>
    <p>{{mail}}</p>
  </div>
</template>

<script>
export default {
    data(){
      return{
        copyRight: "Copyright © www.xxx.edu.cn, All Rights Reserved.",
        mail:"Email : 1621173981@qq.com  QQ: 1621173981"
      }
    }
  }
</script>

<style>
  #footer{
    position: absolute;
    width: 100%;
    bottom: 0px;
    height: 60px;
    line-height: 25px;
    text-align: center;
    background-color: #ffffff;
    z-index: 999;
  }
</style>