let fileElem = document.getElementById('fileElem');
let previewArea = document.getElementById('preview');

fileElem.addEventListener('change', handleFiles, false);

function handleFiles() {
  let files = fileElem.files;
  previewArea.innerHTML = "";
  [...files].forEach(previewFile);
}

function previewFile(file) {
    let reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = function() {
      let img = document.createElement('img')
      img.src = reader.result
      previewArea.appendChild(img)
    }
  }
  

