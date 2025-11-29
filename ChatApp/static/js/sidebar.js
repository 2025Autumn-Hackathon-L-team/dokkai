/*サイドバーの要素をクリックすると、クリックされた要素がactiveとなり、他の要素からactiveを取り除く処理*/

const list = document.querySelectorAll(".navigation ul li");
function activeLink() {
  list.forEach((item) => item.classList.remove("active"));
  this.classList.add("active");
}

list.forEach((item) => {
  item.addEventListener("click", activeLink);
});
