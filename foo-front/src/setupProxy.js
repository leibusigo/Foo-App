const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  app.use(
    '/api/py27',
    createProxyMiddleware({
      target: 'http://127.0.0.1:4018/',
      changeOrigin: true,
    })
  )
  app.use(
    '/api/py36',
    createProxyMiddleware({
      target: 'http://127.0.0.1:4014/',
      changeOrigin: true,
    })
  )
}
