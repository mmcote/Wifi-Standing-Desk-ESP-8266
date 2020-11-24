const { remote } = require('electron')
const storeInstance = remote.getGlobal('db');

const STANDING = "standing";
const SITTING = "sitting";
const IP = "ip";

function setLocalIp(ip) {
  storeInstance.set(IP, ip)
}

function getLocalIp() {
  return storeInstance.get(IP)
}

function setStandingHeight(height) {
  storeInstance.set(STANDING, height);
}

function getStandingHeight() {
  return storeInstance.get(STANDING);
}

function setSittingHeight() {
  storeInstance.set(SITTING, height);
}

function getSittingHeight() {
  return storeInstance.get(SITTING);
}

function adjustToStanding() {
  height = getStandingHeight()
  send('http://' + getLocalIp() + '?height=' + height)
}

function adjustToSitting() {
  height = getSittingHeight()
  send('http://' + getLocalIp() + '?height=' + height)
}

function cancelAdjustment() {
  send('http://' + getLocalIp() + '/cancel')
}

async function getCurrentHeight() {
  console.log("ehRKLDSFLKD")
  return send('http://' + getLocalIp() + '/height')
  .then((resp) => resp.text())
  .then((body) => {
    const reg = '^height:.([0-9]+.[0-9]+)$'; 
    const match = body.match(reg);
    if (match != null) {
      return Math.round(parseFloat(match[1]))
    }
    return 0;
  })
}

async function send(url) {
  return await fetch(url);
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('up').addEventListener('click', () => adjustToStanding());
    document.getElementById('down').addEventListener('click', () => adjustToSitting());
    document.getElementById('cancel').addEventListener('click', () => cancelAdjustment());
    
    document.getElementById('localIp').value = getLocalIp()
    document.getElementById('set-ip').addEventListener('click', () => {
      const localIp = document.getElementById('localIp').value;
      if (localIp === "") {
        return
      }

      setLocalIp(localIp);
    });
   
    const heightLabel = document.getElementById('heightLabel')
    setInterval(()=> getCurrentHeight().then((height) => { 
      heightLabel.innerHTML = height; 
      console.log(height) }), 3000);
});