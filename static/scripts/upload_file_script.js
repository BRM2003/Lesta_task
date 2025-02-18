const form = document.querySelector("form");
const fileInput = document.querySelector(".file-input");

form.addEventListener("click", () =>{
  fileInput.click();
});
fileInput.onchange = ({target})=> {
  if(target.files[0])
      document.FileForm.submit();
}
