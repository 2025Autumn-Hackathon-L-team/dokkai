/*
プロフィールを更新するモーダルの制御
*/

const updateButton = document.getElementById("update-email-button");
const updateProfileEmailModal = document.getElementById("update-profile-email-modal");
const updateProfileEmailButtonClose = document.getElementById(
  "update-email-close-button"
);

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
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
