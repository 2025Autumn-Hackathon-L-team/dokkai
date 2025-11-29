/*プロフィールを更新するモーダルの制御*/

const updateButton = document.getElementById("update-name-button");
const updateProfileNameModal = document.getElementById("update-profile-name-modal");
const updateProfileNameButtonClose = document.getElementById("update-name-close-button");
const flashContentName = document.getElementById('name-modal-flash-content');

// 4秒後にフラッシュメッセージを消去
if (flashContentName && updateProfileNameModal) {
    updateProfileNameModal.style.display = "flex";   
    window.setTimeout(function(){
    flashContentName.remove();
  }, 4000);
}  

// モーダルが存在するページのみ
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
