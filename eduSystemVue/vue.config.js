module.exports = {
    publicPath: './',
    productionSourceMap: true,
    devServer:{
        port:8080,
        host:'localhost',
        open:true,
        // proxy: {
        //     '/api': {
        //         target: 'http://47.93.85.24:8080',
        //         ws: true,
        //         changeOrigin: true,
        //         // pathRewrite: {
        //         //     '^/api': ''  //通过pathRewrite重写地址，将前缀/api转为/
        //         // }
        //     }
        // }
    }
}