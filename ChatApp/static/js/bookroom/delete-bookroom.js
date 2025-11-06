/*
チャンネルを削除するモーダルの制御
*/
const deleteButtons = document.querySelectorAll(".delete-bookroom-trigger"); 
const deleteBookroomModal = document.getElementById("delete-bookroom-modal");
const deletePageButtonClose = document.getElementById("delete-page-close-button");
const deleteBookroomForm = document.getElementById("deleteBookroomForm"); 
const prefix = typeof IS_PUBRIC !== 'undefined' && IS_PUBRIC
    ? '/public_bookrooms'
    : '/private_bookrooms';

if (deleteBookroomModal && deleteBookroomForm) {
  deleteButtons.forEach(button => {
      button.addEventListener("click", () => {
      const bookroomId = button.getAttribute("data-bookroom-id");
        if (bookroomId) {
          const endpoint = `${prefix}/delete/${bookroomId}`; 
          deleteBookroomForm.action = endpoint;
            if (!deleteBookroomForm.querySelector('input[name="_method"][value="DELETE"]')) {
              const methodInput = document.createElement("input");
              methodInput.type = "hidden";
              methodInput.name = "_method";
              methodInput.value = "DELETE";
              deleteBookroomForm.appendChild(methodInput);
              }
              deleteBookroomModal.style.display = "flex";
          } else {
               console.error("Error: ブックルームIDが取得できませんでした。");
          }
      });
  });
  if (deletePageButtonClose) {
    deletePageButtonClose.addEventListener("click", () => {
      deleteBookroomModal.style.display = "none";
    });
  }
  addEventListener("click", (e) => {
    if (e.target === deleteBookroomModal) { 
      deleteBookroomModal.style.display = "none";
    }
  });

}