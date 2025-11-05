/*
チャンネルを削除するモーダルの制御
*/
// 💡 修正点 1: クラスで全てのボタンを取得し、変数を定義
const deleteButtons = document.querySelectorAll(".delete-bookroom-trigger"); 

const deleteBookroomModal = document.getElementById("delete-bookroom-modal");
const deletePageButtonClose = document.getElementById("delete-page-close-button");
const deleteBookroomForm = document.getElementById("deleteBookroomForm"); // フォーム要素を取得

// モーダルとフォームの両方が存在する場合のみ実行
if (deleteBookroomModal && deleteBookroomForm) {
  
  // 💡 修正点 2: 取得した全てのボタンに対してループ処理を行う
  deleteButtons.forEach(button => {
      
      // 各ボタンにクリックイベントを設定
      button.addEventListener("click", () => {
          
          // 1. 押されたボタンからブックルームIDを取得
          const bookroomId = button.getAttribute("data-bookroom-id");
          
          if (bookroomId) {
              // 2. フォームアクションを動的に設定
              const endpoint = `/public_bookrooms/delete/${bookroomId}`; 
              deleteBookroomForm.action = endpoint;

              // 3. _method=DELETE 隠しフィールドの確認と追加（初回のみ）
              if (!deleteBookroomForm.querySelector('input[name="_method"][value="DELETE"]')) {
                  const methodInput = document.createElement("input");
                  methodInput.type = "hidden";
                  methodInput.name = "_method";
                  methodInput.value = "DELETE";
                  deleteBookroomForm.appendChild(methodInput);
              }
              
              // 4. モーダルを表示
              deleteBookroomModal.style.display = "flex";
          } else {
               console.error("Error: ブックルームIDが取得できませんでした。");
          }
      });
  });

  // --- モーダルの非表示制御 ---

  // 3. モーダル非表示イベントリスナーの設定 (Xボタン)
  if (deletePageButtonClose) {
    deletePageButtonClose.addEventListener("click", () => {
      deleteBookroomModal.style.display = "none";
    });
  }

  // 4. モーダル非表示イベントリスナーの設定 (背景クリック)
  addEventListener("click", (e) => {
    if (e.target === deleteBookroomModal) { 
      deleteBookroomModal.style.display = "none";
    }
  });

}