/*
チャンネルを削除するモーダルの制御
*/
if (uid === channel.uid) {
  const deleteButton = document.createElement("button");
          deleteButton.innerHTML =
            '<ion-icon name="trash-bin-outline" style="color: #f57978"></ion-icon>';
          deleteButton.classList.add("delete-button");
          li.appendChild(deleteButton);
          // ゴミ箱ボタンが押された時にdeleteモーダルを表示させる
          deleteButton.addEventListener("click", () => {
            deleteChannelModal.style.display = "flex";

            const deleteChannelForm =
              document.getElementById("deleteChannelForm");

            const endpoint = `/channels/delete/${channel.id}`;
            deleteChannelForm.action = endpoint;
          });
        }

  const deletePageButtonClose = document.getElementById(
    "delete-page-close-button"
  );

  const deleteChannelModal = document.getElementById("delete-channel-modal");

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  deletePageButtonClose.addEventListener("click", () => {
    deleteChannelModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == deleteChannelModal) {
      deleteChannelModal.style.display = "none";
    }
  });