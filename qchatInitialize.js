function qchatInitialize(auth) {
  const qchat = document.createElement("qontak-webchat");
  document.body.appendChild(qchat);
  localStorage.qchat_id = auth.id;
  localStorage.qchat_code = auth.code;
  if (auth.user) localStorage.qchat_user = auth.user;
}
