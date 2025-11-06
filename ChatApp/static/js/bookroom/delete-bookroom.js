/*ブックルームを削除するモーダルの制御*/
const deleteButtons = document.querySelectorAll(".delete-bookroom-trigger"); 
const deleteBookroomModal = document.getElementById("delete-bookroom-modal");
const deletePageButtonClose = document.getElementById("delete-page-close-button");
const deleteBookroomForm = document.getElementById("deleteBookroomForm"); 

/* パブリックフラグがtrueかどうかでprefixを変更する*/
const prefix = typeof IS_PUBRIC !== 'undefined' && IS_PUBRIC
    ? '/public_bookrooms'
    : '/private_bookrooms';

/* HTMLから取得したブックルームIDと上記のprefixでフォームの送信先を決定する*/    
if (deleteBookroomModal && deleteBookroomForm) {
  deleteButtons.forEach(button => {
      button.addEventListener("click", () => {
      const bookroomId = button.getAttribute("data-bookroom-id");
        if (bookroomId) {
          const endpoint = `${prefix}/delete/${bookroomId}`; 
          deleteBookroomForm.action = endpoint;
              deleteBookroomModal.style.display = "flex";
          }});
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