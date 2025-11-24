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