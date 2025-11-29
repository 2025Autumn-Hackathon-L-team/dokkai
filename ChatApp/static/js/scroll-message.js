/*各メッセージ画面読み込み時に自動で最新メッセージまでスクロールする処理*/

function scrollToBottom() {
  const messageArea = document.getElementById("message-area");
  
  if (messageArea) {
    const offset = (16 * window.innerHeight) / 100; 
    const targetScroll = messageArea.scrollHeight - offset;   
    messageArea.scrollTo({
      top: targetScroll,
      behavior: "auto" 
    });
  }
}

window.addEventListener('load', scrollToBottom); 
