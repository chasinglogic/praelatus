'use strict';

var path = require('path');
var glob = require('glob');
var webpack = require('webpack');
var extractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  devtool: 'eval-source-map',
  entry: [
    'jquery',
    'tether',
    'popper.js',
    'moment',
    'select2',
    'bootstrap',
    'simplemde',
    path.join(__dirname, 'frontend/css/index.scss'),
    path.join(__dirname, 'frontend/favicon.ico'),
    path.join(__dirname, 'frontend/js/index.js')
  ].concat(glob.sync('./frontend/img/*')),
  output: {
    path: path.join(__dirname, 'app/static/'),
    filename: 'index.js',
    publicPath: '/'
  },
  plugins: [
    /* Assign the module and chunk ids by occurrence count. Ids that are used
       often get lower (shorter) ids. This make ids predictable reduces total file
       size and is recommended. */
    new webpack.optimize.OccurrenceOrderPlugin(),

    /* Seperate sass styles into a css file */
    new extractTextPlugin('index.css'),

    /* Enables Hot Module Replacement. (This requires records data if not in
       dev-server mode, recordsPath) */
    new webpack.HotModuleReplacementPlugin(),

    /* When there are errors while compiling this plugin skips the emitting
       phase (and recording phase), so there are no frontend emitted that include
       errors. The emitted flag in the stats is false for all frontend. If you are
       using the CLI, the webpack process will not exit with an error code by
       enabling this plugin. If you want webpack to "fail" when using the CLI,
       please check out the bail option. */
    new webpack.NoEmitOnErrorsPlugin(),

    /* Provide jQuery in the way that bootstrap expects */
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      Tether: 'tether',
      Popper: 'popper.js',
      SimpleMDE: 'simplemde'
    })
  ],
  module: {
    rules: [
      {
        test: /\.css$/,
        loader: 'css-loader'
      },
      {
        test: /\.s(c|a)ss$/,
        use: extractTextPlugin.extract({ use: [
          {
            loader: 'css-loader'
          },
          {
            loader: 'sass-loader'
          }
        ]})
      },
      {
        test: /\.(eot|ttf|woff2?|svg|ico)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]'
            }
          }
        ]
      },
    ]
  }
};
