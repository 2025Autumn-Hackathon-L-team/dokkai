/*
チャンネルを更新するモーダルの制御
*/

const updateButton = document.getElementById("bookroom-update-button");
const updateChannelModal = document.getElementById("update-bookroom-modal");
const updatePageButtonClose = document.getElementById(
  "update-page-close-button"
);

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (updateBookroomModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  updateButton.addEventListener("click", () => {
    updateBookroomModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updatePageButtonClose.addEventListener("click", () => {
    updateBookroomModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateBookroomModal) {
      updateBookroomModal.style.display = "none";
    }
  });
}

// update-channel-modalが表示されている時に Ctrl/Command + Enter で送信
function sendUpdateForm() {
  const newBookroomTitle = document.updateBookroomForm.BookroomTitle.value;

  if (newBookroomTitle !== "") {
    document.updateBookroomForm.submit();
  }
}