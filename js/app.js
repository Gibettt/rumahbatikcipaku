window.addEventListener(
  "message",
  function(e) {
    const iframe = document.getElementById("qontak-webchat-widget");
    const { eventName, data } = e.data;
    switch (eventName) {
      case "setFrameSize":
        iframe.height = data.height;
        iframe.width = data.width;
        break;
    }
  },
  false
);
const ifrm = document.createElement("iframe");
const current = document.currentScript;
const source = new URL(current.getAttribute("src"));
const qchatCode = localStorage.getItem("qchat_code");
const qchatId = localStorage.getItem("qchat_id");
const qchatUser = localStorage.getItem("qchat_user");
const qchatDomain = window.location.origin;
const width = window.innerWidth;
const height = window.innerHeight;
ifrm.setAttribute(
  "src",
  `${source.origin}?c=${qchatCode}&i=${qchatId}&d=${qchatDomain}&w=${width}&h=${height}&u=${qchatUser}`
);
ifrm.setAttribute("id", "qontak-webchat-widget");
ifrm.setAttribute("frameborder", "0");
ifrm.setAttribute("allowfullscreen", "true");
ifrm.setAttribute("webkitallowfullscreen", "true");
ifrm.setAttribute("mozallowfullscreen", "true");
ifrm.style.position = "fixed";
ifrm.style.bottom = "0";
ifrm.style.right = "0";
ifrm.style.zIndex = "999999";
ifrm.style.maxHeight = "100%";
ifrm.style.overflow = "auto";
ifrm.width = "94px";
ifrm.height = "94px";
document.body.appendChild(ifrm);
