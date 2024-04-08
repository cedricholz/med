const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  webpack: {
    configure: (webpackConfig, { env, paths }) => {
      webpackConfig.plugins.push(
        new CleanWebpackPlugin(),
        new BundleTracker({ path: __dirname, filename: 'webpack-stats.json' })
      );

      webpackConfig.output = {
        path: path.resolve(__dirname, 'build'),
        filename: 'static/js/[name].js',
        publicPath: 'http://localhost:3000/',
      };

      return webpackConfig;
    },
  },
  devServer: (devServerConfig, { env, paths, proxy, allowedHost }) => {
    devServerConfig.devMiddleware = {
      ...devServerConfig.devMiddleware,
      writeToDisk: true,
    };
    return devServerConfig;
  },
};