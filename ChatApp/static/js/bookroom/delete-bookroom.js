/*
チャンネルを削除するモーダルの制御
*/
const deleteButton = document.getElementById("delete-bookroom-button");
const deleteBookroomModal = document.getElementById("delete-bookroom-modal");
const deletePageButtonClose = document.getElementById("delete-page-close-button");

// モーダルが存在するページのみ（uidとブックルームidが同じ時のみ）
if (deleteBookroomModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  deleteButton.addEventListener("click", () => {
    deleteBookroomModal.style.display = "flex";
  });

  const endpoint = `/public_bookrooms/delete/${bookroom.id}`;
  deleteBookroomForm.action = endpoint;

  const deletePageButtonClose = document.getElementById(
    "delete-page-close-button"
  )
  };
  // モーダル内のXボタンが押された時にモーダルを非表示にする
  deletePageButtonClose.addEventListener("click", () => {
    deleteBookroomModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == deleteBookroomModal) {
      deleteBookroomModal.style.display = "none";
    }
  })