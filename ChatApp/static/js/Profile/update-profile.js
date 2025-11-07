/*
プロフィールを更新するモーダルの制御
*/

const updateButton = document.getElementById("update-profile-button");
const updateProfileModal = document.getElementById("update-profile-modal");
const updatePageButtonClose = document.getElementById(
  "update-page-close-button"
);

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (updateProfileModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  updateButton.addEventListener("click", () => {
    updateProfileModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updatePageButtonClose.addEventListener("click", () => {
    updateProfileModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateProfileModal) {
      updateProfileModal.style.display = "none";
    }
  });
}

// これはprofileにあった方がいいか？
// update-channel-modalが表示されている時に Ctrl/Command + Enter で送信
// function sendUpdateForm() {
//  const newBookroomTitle = document.updateBookroomForm.BookroomTitle.value;

//  if (newBookroomTitle !== "") {
//    document.updateBookroomForm.submit();
//  }
//}