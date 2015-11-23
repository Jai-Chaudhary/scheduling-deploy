var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
var config = require('./webpack.config');

var javaServer = "http://localhost:4567";
var pythonServer = "http://localhost:5000";

new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  hot: true,
  historyApiFallback: true,
  proxy: {
    '/simulate_frames': javaServer,
    '/get_animation_stats': javaServer,
    '/parse_synthetic': javaServer,
    '/evaluate_optimize': javaServer,
    '/get_state': pythonServer,
  }
}).listen(3000, '0.0.0.0', function (err, result) {
  if (err) {
    console.log(err);
  }

  console.log('Listening at 0.0.0.0:3000');
});
