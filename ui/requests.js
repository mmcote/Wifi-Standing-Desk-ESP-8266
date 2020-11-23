const { remote } = require('electron')
const storeInstance = remote.getGlobal('db');

const standing = "standing";
const sitting = "sitting";

const ip = ''

function setStandingHeight(height) {
  storeInstance.set(standing, height);
}

function setSittingHeight() {
  storeInstance.set(sitting, height);
}

function getStandingHeight() {
  return storeInstance.get(standing);
}

function getSittingHeight() {
  return storeInstance.get(sitting);
}

function adjustToStanding() {
  height = getStandingHeight()
  send('http://' + ip + '?height=' + height)
}

function adjustToSitting() {
  height = getSittingHeight()
  send('http://' + ip + '?height=' + height)
}

function cancelAdjustment() {
  send('http://' + ip + '/cancel')
}

async function send(url) {
  const response = await fetch(url);
  console.log(response.status);
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('up').addEventListener('click', () => adjustToStanding());
    document.getElementById('down').addEventListener('click', () => adjustToSitting());
    document.getElementById('cancel').addEventListener('click', () => cancelAdjustment());
});