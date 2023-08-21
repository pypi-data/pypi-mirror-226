const pm2 = require('pm2');
module.exports = {
  list: () => {
    pm2.connect(function(err) {
      if (err) {
        return console.error(err)
      }
      pm2.list((err, details) => {
        pm2.disconnect();
        if (err) {
          return console.error(err)
        }
        return console.log(JSON.stringify(details))
      })
    })
  },
  start: (id) => {
    pm2.connect(function(err) {
      if (err) {
        return console.error(err)
      }
      pm2.start(id, (err, details) => {
        pm2.disconnect();
        if (err) {
          return console.error(err)
        }
        return console.log(JSON.stringify(details))
      })
    })
  },
  stop: (id) => {
    pm2.connect(function(err) {
      if (err) {
        return console.error(err)
      }
      pm2.stop(id, (err, details) => {
        pm2.disconnect();
        if (err) {
          return console.error(err)
        }
        return console.log(JSON.stringify(details))
      })
    })
  },
  restart: (id) => {
    pm2.connect(function(err) {
      if (err) {
        return console.log(err)
      }
      pm2.restart(id, (err, details) => {
        pm2.disconnect();
        if (err) {
          return console.error(err)
        }
        return console.log(JSON.stringify(details))
      })
    })
  },
  reload: (id) => {
    pm2.connect(function(err) {
      if (err) {
        return console.log(err)
      }
      pm2.reload(id, (err, details) => {
        pm2.disconnect();
        if (err) {
          return console.error(err)
        }
        return console.log(JSON.stringify(details))
      })
    })
  },
  delete: (id) => {
    pm2.connect(function(err) {
      if (err) {
        return console.error(err)
      }
      pm2.delete(id, (err, details) => {
        pm2.disconnect();
        if (err) {
          return console.error(err)
        }
        return console.log(JSON.stringify(details))
      })
    })
  },
  kill: () => {
    pm2.connect(function(err) {
      if (err) {
        return console.error(err)
      }
      pm2.killDaemon((err, details) => {
        if (err) {
          return console.error(err)
        }
        return console.log(JSON.stringify(details))
      })
    })
  },
  describe: (id) => {
    pm2.connect(function(err) {
      if (err) {
        return console.error(err)
      }
      pm2.describe(id, (err, details) => {
        pm2.disconnect();
        if (err) {
          return console.error(err);
        }
        return console.log(JSON.stringify(details))
      })
    })
  }
};
