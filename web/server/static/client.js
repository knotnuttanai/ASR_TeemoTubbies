// peer connection
var pc = null;
var dc = null,
  dcInterval = null;

// Setup Styles
document
  .getElementById("application")
  .setAttribute("style", "height:" + document.body.clientHeight);

transcriptionOutput = document.getElementById("output");
equationBox = document.getElementById("equation");
answerBox = document.getElementById("answer");
start_btn = document.getElementById("start");
stop_btn = document.getElementById("stop");
statusField = document.getElementById("status");
line = document.getElementById("line");
submitButton = document.getElementById("submit");
textarea = document.getElementById("textarea");

var lastWord = "";

var lastTrans = document.createElement("span");
lastTrans.innerText = "💤";
lastTrans.classList.add("partial");
transcriptionOutput.appendChild(lastTrans);
var imcompleteTrans = "";

function btn_show_stop() {
  start_btn.classList.add("d-none");
  stop_btn.classList.remove("d-none");
}

function btn_show_start() {
  stop_btn.classList.add("d-none");
  start_btn.classList.remove("d-none");
  //   lastTrans.innerText = "💤";
  statusField.innerText = "";
}

textarea.onfocus = () => {
  submitButton.classList.remove("d-none");
};

function negotiate() {
  return pc
    .createOffer()
    .then(function (offer) {
      return pc.setLocalDescription(offer);
    })
    .then(function () {
      return new Promise(function (resolve) {
        if (pc.iceGatheringState === "complete") {
          resolve();
        } else {
          function checkState() {
            if (pc.iceGatheringState === "complete") {
              pc.removeEventListener("icegatheringstatechange", checkState);
              resolve();
            }
          }

          pc.addEventListener("icegatheringstatechange", checkState);
        }
      });
    })
    .then(function () {
      var offer = pc.localDescription;
      //console.log(offer.sdp);
      return fetch("/offer", {
        body: JSON.stringify({
          sdp: offer.sdp,
          type: offer.type,
        }),
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
      });
    })
    .then(function (response) {
      return response.json();
    })
    .then(function (answer) {
      //console.log(answer.sdp);
      return pc.setRemoteDescription(answer);
    })
    .catch(function (e) {
      //console.log(e);
      btn_show_start();
    });
}

function start() {
  btn_show_stop();

  // clear textarea
  textarea.value = "";
  textarea.classList.add("d-none");
  transcriptionOutput.classList.remove("d-none");

  line.classList.add("d-none");
  submitButton.classList.add("d-none");

  lastTrans.innerText = "💤";
  statusField.innerText = "Connecting...";
  equationBox.innerText = "";
  answerBox.innerText = "";

  var config = {
    sdpSemantics: "unified-plan",
  };

  pc = new RTCPeerConnection(config);

  var parameters = {};

  dc = pc.createDataChannel("chat", parameters);
  dc.onclose = function () {
    clearInterval(dcInterval);
    //console.log('Closed data channel');
    btn_show_start();
  };
  dc.onopen = function () {
    //console.log('Opened data channel');
  };
  dc.onmessage = function (evt) {
    statusField.innerText = "Listening...";
    var msg = evt.data;

    if (msg.endsWith("\n")) {
      lastTrans.innerText = imcompleteTrans + msg.substring(0, msg.length - 1);

      lastTrans.classList.remove("partial");
      lastTrans = document.createElement("span");
      lastTrans.classList.add("partial");
      lastTrans.innerText = "...";
      transcriptionOutput.appendChild(lastTrans);

      imcompleteTrans = "";
    } else if (msg.endsWith("\r")) {
      lastTrans.innerText =
        imcompleteTrans + msg.substring(0, msg.length - 1) + "...";
      imcompleteTrans = "";
    } else {
      imcompleteTrans += msg;
    }
  };

  pc.oniceconnectionstatechange = function () {
    if (pc.iceConnectionState == "disconnected") {
      //console.log('Disconnected');
      btn_show_start();
    }
  };

  var constraints = {
    audio: true,
    video: false,
  };

  navigator.mediaDevices.getUserMedia(constraints).then(
    function (stream) {
      stream.getTracks().forEach(function (track) {
        pc.addTrack(track, stream);
      });
      return negotiate();
    },
    function (err) {
      //console.log('Could not acquire media: ' + err);
      btn_show_start();
    }
  );
}

function manualSubmit() {
  fetch("/text2num", {
    body: JSON.stringify({
      text: textarea.value,
    }),
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data) {
        equationBox.innerText = data.equation;
        answerBox.innerText = data.ans;
        line.classList.remove("d-none");
      }
    });

  closeChannels();
}

function stop() {
  fetch("/text2num", {
    body: JSON.stringify({
      text: transcriptionOutput.textContent,
    }),
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data) {
        equationBox.innerText = data.equation;
        answerBox.innerText = data.ans;
        line.classList.remove("d-none");
      }
    });
  // copy text over to textarea to make it editable
  textarea.classList.remove("d-none");
  transcriptionOutput.classList.add("d-none");
  textarea.value = transcriptionOutput.textContent;
  lastTrans.innerText = "";

  closeChannels();
}

function closeChannels() {
  // close data channel
  if (dc) {
    dc.close();
  }

  // close transceivers
  if (pc.getTransceivers) {
    pc.getTransceivers().forEach(function (transceiver) {
      if (transceiver.stop) {
        transceiver.stop();
      }
    });
  }

  // close local audio / video
  pc.getSenders().forEach(function (sender) {
    sender.track.stop();
  });

  // close peer connection
  setTimeout(function () {
    pc.close();
  }, 500);
}
