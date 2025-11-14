/*ブックルームを新規作成するモーダルの制御*/

  const createBookroomModal = document.getElementById("create-bookroom-modal");
  const addPageButtonClose = document.getElementById("add-page-close-button");
  const createBookroomButton = document.getElementById("create-bookroom-button");
  
  const flashContent = document.getElementById('modal-flash-content');
  if (flashContent) {
    window.setTimeout(function(){
    flashContent.remove();
  }, 4000);
}
  // モーダル表示ボタンが押された時にモーダルを表示する

  createBookroomButton.addEventListener("click", () => {
    createBookroomModal.style.display = "flex";
  }
  );
  // モーダル内のXボタンが押された時にモーダルを非表示にする
  addPageButtonClose.addEventListener("click", () => {
    createBookroomModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target === createBookroomModal) {
      createBookroomModal.style.display = "none";
    }
  });

  // create-bookroom-modalが表示されている時に Ctrl/Command + Enterで送信
  // Enterで自動送信を防ぐ
  document.addEventListener("keydown", keydownEvent);

  function keydownEvent(e) {
    const newBookroomTitle = document.createBookroomForm.bookroomTitle.value;

    const createBookroomModal = document.getElementById("create-bookroom-modal");
    const createBookroomModalStyle = getComputedStyle(
      createBookroomModal,
      null
    ).getPropertyValue("display");

    if (e.code === "Enter") {
      e.preventDefault();
    }

    if (
      ((e.ctrlKey && !e.metaKey) || (!e.ctrlKey && e.metaKey)) &&
      e.keyCode == 13
    ) {
      if (e.code === "Enter") {
        if (createBookroomModalStyle !== "none") {
          if (newBookroomTitle !== "") {
            document.createBookroomForm.submit();
          }
        }
      }
    }
  }
