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

async function send(url) {
  const response = await fetch(url);
  console.log(response.status);
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
});