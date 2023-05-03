export function prepareSocket(host = window.location.host) {
  let socket = io("wss://" + host);
  socket.on("connect", () => {
    console.log("connected");
  });
  socket.on("message", (data) => {
    console.log(data);
  });
  return socket;
}

export async function getConnectedDevices(type="videoinput") {
  const devices = await navigator.mediaDevices.enumerateDevices();
  return devices.filter((device) => device.kind === type);
}
/**
 * Asynchronously plays a video stream from the user's camera on a video element with
 * the ID 'localVideo' using the WebRTC API.
 *
 * @returns {Promise<void>} A promise that resolves when the video stream starts playing.
 * @throws {Error} If there is an error opening the camera or setting up the video element.
 */
export async function playVideoFromCamera() {
  try {
    const constraints = { video: true, audio: false };
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    const videoElement = document.querySelector("video#localVideo");
    videoElement.srcObject = stream;
  } catch (error) {
    console.error("Error opening video camera.", error);
  }
}
/**
 * Asynchronously plays and displays media from the user's screen.
 *
 * @async
 * @function playDisplayMedia
 * @throws {Error} If there is an error opening the video camera.
 * @returns {Promise<void>} Promise resolved with no value once media is displayed.
 */
export async function playDisplayMedia() {
  try {
    const constraints = {
      video: {
        cursor: "always",
        displaySurface: "monitor",
      },
      audio: false,
    };
    const stream = await navigator.mediaDevices.getDisplayMedia(constraints);
    const videoElement = document.querySelector("video#localVideo");
    videoElement.srcObject = stream;
  } catch (error) {
    console.error("Error opening video camera.", error);
  }
}

export async function playAllVideoInput(parentElement = document.body) {
  const vidlist = document.createElement("div");
  vidlist.id = "vidlist";
  parentElement.appendChild(vidlist);

  const devices = await getConnectedDevices("videoinput");
  for (let i = 0; i < devices.length; i++) {
    let stream = await navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: devices[i].deviceId,
      },
    });
    try {
      let video = document.createElement("video");
      video.id = "video" + i;
      video.srcObject = stream;
      video.autoplay = true;
      video.playsInline = true;
      video.controls = false;
      vidlist.appendChild(video);
    } catch (error) {
      console.error("Error opening video camera.", error);
    }
  }
}
