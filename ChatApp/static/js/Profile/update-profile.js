/*
プロフィールを更新するモーダルの制御
*/

const updateButton = document.getElementById("update-profile-button");
const updateProfileModal = document.getElementById("update-profile-modal");
const updateProfileButtonClose = document.getElementById(
  "update-profile-close-button"
);

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (updateProfileModal) {
   const flashContent = document.getElementById('modal-flash-content');

  if (flashContent) {
    // Flashメッセージが存在すれば、モーダルを強制的に表示する
    // updateProfileModal.style.display = "flex"; のロジックを再利用
    updateProfileModal.style.display = "flex";
    window.setTimeout(function(){
    flashContent.remove();
  }, 4000);
  }
    window.setTimeout(function(){
    flashContent.remove();
  }, 4000);
  }
  // モーダル表示ボタンが押された時にモーダルを表示する
  updateButton.addEventListener("click", () => {
    updateProfileModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updateProfileButtonClose.addEventListener("click", () => {
    updateProfileModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateProfileModal) {
      updateProfileModal.style.display = "none";
    }
  });


// これはprofileにあった方がいいか？
// update-channel-modalが表示されている時に Ctrl/Command + Enter で送信
// function sendUpdateForm() {
//  const newBookroomTitle = document.updateBookroomForm.BookroomTitle.value;

//  if (newBookroomTitle !== "") {
//    document.updateBookroomForm.submit();
//  }
//}