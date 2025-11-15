/*
プロフィールを更新するモーダルの制御
*/

const updateButton = document.getElementById("update-name-button");
const updateProfileNameModal = document.getElementById("update-profile-name-modal");
const updateProfileNameButtonClose = document.getElementById("update-name-close-button");
const flashContent = document.getElementById('modal-flash-content');

if (flashContent && updateProfileModal) {
    updateProfileModal.style.display = "flex";   
    window.setTimeout(function(){
    flashContent.remove();
  }, 4000);
}  

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (updateProfileNameModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  updateButton.addEventListener("click", () => {
    updateProfileNameModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updateProfileNameButtonClose.addEventListener("click", () => {
    updateProfileNameModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateProfileNameModal) {
      updateProfileNameModal.style.display = "none";
    }
  });
}
