/*プロフィールを更新するモーダルの制御*/

const updateButton = document.getElementById("update-email-button");
const updateProfileEmailModal = document.getElementById("update-profile-email-modal");
const updateProfileEmailButtonClose = document.getElementById("update-email-close-button");
const flashContentEmail = document.getElementById('email-modal-flash-content');

// 4秒後にフラッシュメッセージを消去
if (flashContentEmail && updateProfileEmailModal) {
    updateProfileEmailModal.style.display = "flex";   
    window.setTimeout(function(){
    flashContentEmail.remove();
  }, 4000);
}  
// モーダルが存在するページのみ
if (updateProfileEmailModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  updateButton.addEventListener("click", () => {
    updateProfileEmailModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updateProfileEmailButtonClose.addEventListener("click", () => {
    updateProfileEmailModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateProfileEmailModal) {
      updateProfileEmailModal.style.display = "none";
    }
  });
}
