/*
チャンネルを削除するモーダルの制御
*/
const deleteButton = document.getElementById("delete-bookroom-button");
const deleteBookroomModal = document.getElementById("delete-bookroom-modal");
const deletePageButtonClose = document.getElementById("delete-page-close-button");
const deleteBookroomForm = document.getElementById("deleteBookroomForm")

if (deleteBookroomModal) {
  // モーダルが存在するページのみ（uidとブックルームidが同じ時のみ）
   if (typeof bookroom !== 'undefined' && bookroom.id) {
    const endpoint = `/public_bookrooms/delete/${bookroom.id}`; 
    deleteBookroomForm.action = endpoint;
    if (!deleteBookroomForm.querySelector('input[name="_method"][value="DELETE"]')) {
      const methodInput = document.createElement("input");
      methodInput.type = "hidden";
      methodInput.name = "_method";
      methodInput.value = "DELETE";
      deleteBookroomForm.appendChild(methodInput);
    }
  } else {
      // bookroom.idがない場合、フォーム送信を避けるなどの安全策を講じることが推奨されます
      console.error("Error: bookroom.id is undefined or not available.");
  }
  }
  // モーダル表示ボタンが押された時にモーダルを表示する
  deleteButton.addEventListener("click", () => {
    deleteBookroomModal.style.display = "flex";
  });

  if (deletePageButtonClose) {
    deletePageButtonClose.addEventListener("click", () => {
      deleteBookroomModal.style.display = "none";
    });
  }

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == deleteBookroomModal) {
      deleteBookroomModal.style.display = "none";
    }
  });
