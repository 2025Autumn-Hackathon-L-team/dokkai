/*
アイコンを更新するモーダルの制御
*/

const updateIconButton = document.getElementById("update-icon-button");
const updateIconModal = document.getElementById("update-icon-modal");
const updateIconButtonClose = document.getElementById("update-icon-close-button");

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (updateIconModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  updateIconButton.addEventListener("click", () => {
    updateIconModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updateIconButtonClose.addEventListener("click", () => {
    updateIconModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateIconModal) {
      updateIconModal.style.display = "none";
    }
  });
}

  // アイコンが押されたときに
  // document.getElementById('myButton').addEventListener('click', function() {
  // ここでPythonにリクエストを送信する
  // 例：Fetch APIを使用する
  // fetch('/process', { method: 'POST', // またはGET
  //  body: JSON.stringify({ message: 'ボタンが押されました' })

// これはprofileにあった方がいいか？
// update-channel-modalが表示されている時に Ctrl/Command + Enter で送信
// function sendUpdateForm() {
//  const newBookroomTitle = document.updateBookroomForm.BookroomTitle.value;

//  if (newBookroomTitle !== "") {
//    document.updateBookroomForm.submit();
//  }
//}