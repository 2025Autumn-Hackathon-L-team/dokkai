/*
各ブックルーム詳細ページ内、ページ読み込み時に自動で下までスクロールする
*/

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
