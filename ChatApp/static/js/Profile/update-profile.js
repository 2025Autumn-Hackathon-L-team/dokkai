/*
プロフィールを更新するモーダルの制御
*/

const updateButton = document.getElementById("update-profile-button");
const updateProfileModal = document.getElementById("update-profile-modal");
const updateProfileButtonClose = document.getElementById("update-profile-close-button");
const flashContent = document.getElementById('modal-flash-content');

if (flashContent && updateProfileModal) {
    updateProfileModal.style.display = "flex";   
    window.setTimeout(function(){
    flashContent.remove();
  }, 4000);
}  

if (updateProfileModal) {  
  // 必須の追加: モーダル表示ボタンのイベントリスナー
  updateButton.addEventListener("click", () => {
    updateProfileModal.style.display = "flex";
  });  
}
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