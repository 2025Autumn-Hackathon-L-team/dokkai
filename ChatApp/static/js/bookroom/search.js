/*検索窓を表示するモーダルの制御*/

  const searchBookroomModal = document.getElementById("search-modal");
  const searchPageButtonClose = document.getElementById("search-page-close-button");
  const searchBookroomButton = document.getElementById("search-button");
  const keywordModalInput = document.getElementById("keyword");
  /*const flashContent = document.getElementById('modal-flash-content');

  if (flashContent) {
    searchBookroomModal.style.display = "flex";
    window.setTimeout(function(){
    flashContent.remove();
  }, 4000);
}*/
  // モーダル表示ボタンが押された時にモーダルを表示する
  searchBookroomButton.addEventListener("click", () => {
    searchBookroomModal.style.display = "flex";
  });
  // モーダル内のXボタンが押された時にモーダルを非表示にする
  searchPageButtonClose.addEventListener("click", () => {
    searchBookroomModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  searchEventListener("click", (e) => {
    if (e.target == searchBookroomModal) {
      searchBookroomModal.style.display = "none";
    }
  });